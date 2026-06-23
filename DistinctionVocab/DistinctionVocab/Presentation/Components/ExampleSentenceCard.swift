import SwiftUI

struct ExampleSentenceCard: View {
    let exampleSentence: ExampleSentence
    var isResolvingMissingText = false

    private var isWaitingForText: Bool {
        isResolvingMissingText && (exampleSentence.text == nil || exampleSentence.text?.isEmpty == true)
    }

    var body: some View {
        HStack(alignment: .top, spacing: 16) {
            VStack(alignment: .leading, spacing: 8) {
                Text("例文 \(exampleSentence.label)")
                    .font(.caption.weight(.semibold))
                    .foregroundStyle(.secondary)

                if isWaitingForText {
                    HStack(spacing: 8) {
                        ProgressView()
                            .controlSize(.small)
                        Text("例文を認識中…")
                            .font(.subheadline)
                            .foregroundStyle(.secondary)
                    }
                } else if let englishText = exampleSentence.text, !englishText.isEmpty {
                    Text(englishText)
                        .font(.body)
                        .fixedSize(horizontal: false, vertical: true)

                    if let japaneseTranslation = exampleSentence.displayJapaneseTranslation {
                        Text(japaneseTranslation)
                            .font(.subheadline)
                            .foregroundStyle(.secondary)
                            .fixedSize(horizontal: false, vertical: true)
                    }
                } else {
                    Text("音声を再生して例文を確認できます")
                        .font(.subheadline)
                        .foregroundStyle(.secondary)
                }
            }

            Spacer(minLength: 12)

            AudioPlayButton(
                audioResource: exampleSentence.audioResource,
                iconSize: 40,
                tintColor: .primary
            )
        }
        .padding(16)
        .background(
            RoundedRectangle(cornerRadius: 16, style: .continuous)
                .fill(Color(.secondarySystemGroupedBackground))
        )
    }
}
