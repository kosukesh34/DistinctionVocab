import Foundation

protocol TranscriptionCacheRepositoryProtocol: Sendable {
    func cachedText(for resource: AudioResourceReference) -> String?
    func saveText(_ text: String, for resource: AudioResourceReference)
}
