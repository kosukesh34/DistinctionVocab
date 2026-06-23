import Foundation

protocol AudioTranscriptionServiceProtocol: Sendable {
    func transcribe(resource: AudioResourceReference) async throws -> String
}

enum TranscriptionError: LocalizedError {
    case audioFileNotFound
    case speechRecognitionUnavailable
    case speechRecognitionDenied
    case emptyTranscriptionResult

    var errorDescription: String? {
        switch self {
        case .audioFileNotFound:
            return "音声ファイルが見つかりません"
        case .speechRecognitionUnavailable:
            return "音声認識が利用できません"
        case .speechRecognitionDenied:
            return "音声認識の権限がありません"
        case .emptyTranscriptionResult:
            return "例文を認識できませんでした"
        }
    }
}
