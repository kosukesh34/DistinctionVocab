import Foundation
import Speech

final class SpeechAudioTranscriptionService: AudioTranscriptionServiceProtocol, @unchecked Sendable {
    private let audioResourceRepository: AudioResourceRepositoryProtocol

    init(audioResourceRepository: AudioResourceRepositoryProtocol) {
        self.audioResourceRepository = audioResourceRepository
    }

    func transcribe(resource: AudioResourceReference) async throws -> String {
        guard let audioFileURL = audioResourceRepository.resolveURL(for: resource) else {
            throw TranscriptionError.audioFileNotFound
        }

        try await requestSpeechAuthorizationIfNeeded()

        guard let speechRecognizer = SFSpeechRecognizer(locale: Locale(identifier: "en-US")),
              speechRecognizer.isAvailable else {
            throw TranscriptionError.speechRecognitionUnavailable
        }

        return try await withCheckedThrowingContinuation { continuation in
            let recognitionRequest = SFSpeechURLRecognitionRequest(url: audioFileURL)
            recognitionRequest.shouldReportPartialResults = false
            if speechRecognizer.supportsOnDeviceRecognition {
                recognitionRequest.requiresOnDeviceRecognition = true
            }

            speechRecognizer.recognitionTask(with: recognitionRequest) { result, error in
                if let error {
                    continuation.resume(throwing: error)
                    return
                }

                guard let result, result.isFinal else { return }

                let transcribedText = result.bestTranscription.formattedString
                    .trimmingCharacters(in: .whitespacesAndNewlines)

                if transcribedText.isEmpty {
                    continuation.resume(throwing: TranscriptionError.emptyTranscriptionResult)
                } else {
                    continuation.resume(returning: transcribedText)
                }
            }
        }
    }

    private func requestSpeechAuthorizationIfNeeded() async throws {
        let authorizationStatus = SFSpeechRecognizer.authorizationStatus()
        if authorizationStatus == .authorized { return }

        if authorizationStatus == .denied || authorizationStatus == .restricted {
            throw TranscriptionError.speechRecognitionDenied
        }

        let newStatus = await withCheckedContinuation { continuation in
            SFSpeechRecognizer.requestAuthorization { status in
                continuation.resume(returning: status)
            }
        }

        guard newStatus == .authorized else {
            throw TranscriptionError.speechRecognitionDenied
        }
    }
}
