#!/usr/bin/env swift
import Foundation
import Speech

struct TranscriptionJob: Codable {
    let audioPath: String
    let outputKey: String
}

@MainActor
final class BatchTranscriber {
    private let audioRoot: URL
    private var cache: [String: String]

    init(audioRoot: URL, cacheURL: URL) {
        self.audioRoot = audioRoot
        if let data = try? Data(contentsOf: cacheURL),
           let decoded = try? JSONDecoder().decode([String: String].self, from: data) {
            self.cache = decoded
        } else {
            self.cache = [:]
        }
        self.cacheURL = cacheURL
    }

    private let cacheURL: URL

    func transcribe(jobs: [TranscriptionJob]) async throws -> [String: String] {
        try await requestAuthorization()

        guard let recognizer = SFSpeechRecognizer(locale: Locale(identifier: "en-US")),
              recognizer.isAvailable else {
            throw NSError(domain: "Transcriber", code: 1, userInfo: [
                NSLocalizedDescriptionKey: "Speech recognition unavailable"
            ])
        }

        var completed = 0
        let total = jobs.count

        for job in jobs {
            if let cached = cache[job.outputKey] {
                cache[job.outputKey] = cached
                continue
            }

            let fileURL = audioRoot.appendingPathComponent(job.audioPath)
            guard FileManager.default.fileExists(atPath: fileURL.path) else { continue }

            do {
                let text = try await transcribeFile(at: fileURL, using: recognizer)
                cache[job.outputKey] = text
                completed += 1
                if completed % 25 == 0 {
                    try saveCache()
                    fputs("  transcribed \(completed)/\(total)\n", stderr)
                }
            } catch {
                fputs("  failed \(job.outputKey): \(error.localizedDescription)\n", stderr)
            }
        }

        try saveCache()
        return cache
    }

    private func requestAuthorization() async throws {
        let status = SFSpeechRecognizer.authorizationStatus()
        if status == .authorized { return }
        if status == .denied || status == .restricted {
            throw NSError(domain: "Transcriber", code: 2, userInfo: [
                NSLocalizedDescriptionKey: "Speech recognition denied"
            ])
        }

        let newStatus = await withCheckedContinuation { continuation in
            SFSpeechRecognizer.requestAuthorization { continuation.resume(returning: $0) }
        }
        guard newStatus == .authorized else {
            throw NSError(domain: "Transcriber", code: 2, userInfo: [
                NSLocalizedDescriptionKey: "Speech recognition denied"
            ])
        }
    }

    private func transcribeFile(at url: URL, using recognizer: SFSpeechRecognizer) async throws -> String {
        try await withCheckedThrowingContinuation { continuation in
            let request = SFSpeechURLRecognitionRequest(url: url)
            request.shouldReportPartialResults = false
            if recognizer.supportsOnDeviceRecognition {
                request.requiresOnDeviceRecognition = true
            }

            recognizer.recognitionTask(with: request) { result, error in
                if let error {
                    continuation.resume(throwing: error)
                    return
                }
                guard let result, result.isFinal else { return }
                let text = result.bestTranscription.formattedString
                    .trimmingCharacters(in: .whitespacesAndNewlines)
                if text.isEmpty {
                    continuation.resume(throwing: NSError(domain: "Transcriber", code: 3))
                } else {
                    continuation.resume(returning: text)
                }
            }
        }
    }

    private func saveCache() throws {
        let data = try JSONEncoder().encode(cache)
        try FileManager.default.createDirectory(
            at: cacheURL.deletingLastPathComponent(),
            withIntermediateDirectories: true
        )
        try data.write(to: cacheURL, options: .atomic)
    }
}

let args = CommandLine.arguments
guard args.count >= 4 else {
    fputs("Usage: transcribe_examples.swift <audio_root> <jobs_json> <cache_json>\n", stderr)
    exit(1)
}

let audioRoot = URL(fileURLWithPath: args[1])
let jobsURL = URL(fileURLWithPath: args[2])
let cacheURL = URL(fileURLWithPath: args[3])

let jobsData = try Data(contentsOf: jobsURL)
let jobs = try JSONDecoder().decode([TranscriptionJob].self, from: jobsData)

let transcriber = await BatchTranscriber(audioRoot: audioRoot, cacheURL: cacheURL)
let result = try await transcriber.transcribe(jobs: jobs)
let outputData = try JSONEncoder().encode(result)
FileHandle.standardOutput.write(outputData)
