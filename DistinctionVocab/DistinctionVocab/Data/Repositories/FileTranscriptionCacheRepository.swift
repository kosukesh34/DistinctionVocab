import Foundation

final class FileTranscriptionCacheRepository: TranscriptionCacheRepositoryProtocol, @unchecked Sendable {
    private let cacheFileURL: URL
    private let lock = NSLock()
    private var inMemoryCache: [String: String] = [:]

    init(cacheFileURL: URL? = nil) {
        let defaultURL = FileManager.default
            .urls(for: .applicationSupportDirectory, in: .userDomainMask)[0]
            .appendingPathComponent("DistinctionVocab/transcriptions.json")
        self.cacheFileURL = cacheFileURL ?? defaultURL
        loadCacheFromDisk()
    }

    func cachedText(for resource: AudioResourceReference) -> String? {
        lock.lock()
        defer { lock.unlock() }
        return inMemoryCache[resource.relativePath]
    }

    func saveText(_ text: String, for resource: AudioResourceReference) {
        lock.lock()
        inMemoryCache[resource.relativePath] = text
        let snapshot = inMemoryCache
        lock.unlock()

        persistCache(snapshot)
    }

    private func loadCacheFromDisk() {
        guard FileManager.default.fileExists(atPath: cacheFileURL.path) else { return }

        do {
            let data = try Data(contentsOf: cacheFileURL)
            inMemoryCache = try JSONDecoder().decode([String: String].self, from: data)
        } catch {
            print("Failed to load transcription cache: \(error)")
        }
    }

    private func persistCache(_ snapshot: [String: String]) {
        do {
            try FileManager.default.createDirectory(
                at: cacheFileURL.deletingLastPathComponent(),
                withIntermediateDirectories: true
            )
            let data = try JSONEncoder().encode(snapshot)
            try data.write(to: cacheFileURL, options: .atomic)
        } catch {
            print("Failed to save transcription cache: \(error)")
        }
    }
}
