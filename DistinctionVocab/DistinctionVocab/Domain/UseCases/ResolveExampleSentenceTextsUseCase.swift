import Foundation

protocol ResolveExampleSentenceTextsUseCaseProtocol: Sendable {
    func execute(for exampleSentences: [ExampleSentence]) async -> [ExampleSentence]
}

/// カタログの例文にテキストが無い場合、音声認識で補完する。
struct ResolveExampleSentenceTextsUseCase: ResolveExampleSentenceTextsUseCaseProtocol {
    private let transcribeAudioUseCase: TranscribeAudioUseCaseProtocol

    init(transcribeAudioUseCase: TranscribeAudioUseCaseProtocol) {
        self.transcribeAudioUseCase = transcribeAudioUseCase
    }

    func execute(for exampleSentences: [ExampleSentence]) async -> [ExampleSentence] {
        guard !exampleSentences.isEmpty else { return [] }

        return await withTaskGroup(of: (Int, ExampleSentence).self, returning: [ExampleSentence].self) { group in
            for (index, exampleSentence) in exampleSentences.enumerated() {
                group.addTask {
                    let resolvedSentence = await resolve(exampleSentence)
                    return (index, resolvedSentence)
                }
            }

            var resolvedSentences = Array(repeating: exampleSentences.first!, count: exampleSentences.count)
            for await (index, sentence) in group {
                resolvedSentences[index] = sentence
            }
            return resolvedSentences
        }
    }

    private func resolve(_ exampleSentence: ExampleSentence) async -> ExampleSentence {
        if let existingText = exampleSentence.text, !existingText.isEmpty {
            return exampleSentence
        }

        guard let transcribedText = await transcribeAudioUseCase.execute(
            resource: exampleSentence.audioResource
        ) else {
            return exampleSentence
        }

        return ExampleSentence(
            label: exampleSentence.label,
            audioResource: exampleSentence.audioResource,
            text: transcribedText,
            japaneseTranslation: exampleSentence.japaneseTranslation
        )
    }
}
