import Foundation

protocol TranscribeAudioUseCaseProtocol: Sendable {
    func execute(resource: AudioResourceReference) async -> String?
}

struct TranscribeAudioUseCase: TranscribeAudioUseCaseProtocol {
    private let audioTranscriptionService: AudioTranscriptionServiceProtocol
    private let transcriptionCacheRepository: TranscriptionCacheRepositoryProtocol

    init(
        audioTranscriptionService: AudioTranscriptionServiceProtocol,
        transcriptionCacheRepository: TranscriptionCacheRepositoryProtocol
    ) {
        self.audioTranscriptionService = audioTranscriptionService
        self.transcriptionCacheRepository = transcriptionCacheRepository
    }

    func execute(resource: AudioResourceReference) async -> String? {
        if let cachedText = transcriptionCacheRepository.cachedText(for: resource) {
            return cachedText
        }

        do {
            let transcribedText = try await audioTranscriptionService.transcribe(resource: resource)
            transcriptionCacheRepository.saveText(transcribedText, for: resource)
            return transcribedText
        } catch {
            print("Transcription failed for \(resource.relativePath): \(error)")
            return nil
        }
    }
}
