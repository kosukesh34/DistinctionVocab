import SwiftUI

struct DistinctionExampleRow: View {
    let exampleSentence: ExampleSentence
    var headword: String? = nil
    @Environment(AVAudioPlaybackService.self) private var audioPlaybackService

    private var isPlaying: Bool {
        audioPlaybackService.isPlaying
            && audioPlaybackService.currentlyPlayingResourcePath == exampleSentence.audioResource.relativePath
    }

    var body: some View {
        Button {
            audioPlaybackService.toggle(resource: exampleSentence.audioResource)
        } label: {
            HStack(alignment: .top, spacing: DistinctionTheme.Spacing.md) {
                Text(exampleSentence.label)
                    .font(.system(size: 13, weight: .bold, design: .rounded))
                    .foregroundStyle(labelColor)
                    .frame(width: 30, height: 30)
                    .background(Circle().fill(labelColor.opacity(0.14)))

                VStack(alignment: .leading, spacing: 6) {
                    if exampleSentence.isParaphrase {
                        tag("言い換え", color: DistinctionTheme.accent)
                    }

                    Group {
                        if exampleSentence.isParaphrase {
                            Text(exampleSentence.displayText)
                        } else {
                            Text(highlightedText)
                        }
                    }
                    .font(DistinctionTheme.exampleEnglishFont)
                    .foregroundStyle(.primary)
                    .multilineTextAlignment(.leading)
                    .fixedSize(horizontal: false, vertical: true)
                    .lineSpacing(2)

                    if let japaneseTranslation = exampleSentence.displayJapaneseTranslation {
                        Text(japaneseTranslation)
                            .font(DistinctionTheme.exampleJapaneseFont)
                            .foregroundStyle(exampleSentence.isParaphrase ? DistinctionTheme.accent : .secondary)
                            .multilineTextAlignment(.leading)
                            .fixedSize(horizontal: false, vertical: true)
                    }
                }

                Spacer(minLength: 4)

                Image(systemName: isPlaying ? "speaker.wave.3.fill" : "speaker.wave.2")
                    .font(.body)
                    .foregroundStyle(isPlaying ? DistinctionTheme.accent : Color(.tertiaryLabel))
                    .frame(width: 24)
                    .symbolEffect(.variableColor.iterative, isActive: isPlaying)
            }
            .contentShape(Rectangle())
        }
        .buttonStyle(.plain)
        .padding(.horizontal, DistinctionTheme.Spacing.lg)
        .padding(.vertical, DistinctionTheme.Spacing.md)
    }

    private func tag(_ text: String, color: Color) -> some View {
        Text(text)
            .font(.caption2.weight(.semibold))
            .foregroundStyle(color)
            .padding(.horizontal, 8)
            .padding(.vertical, 2)
            .background(Capsule().fill(color.opacity(0.14)))
    }

    private var labelColor: Color {
        DistinctionTheme.accent
    }

    // Distinction-style: emphasize the headword inside example sentences (B/C only).
    private var highlightedText: AttributedString {
        let sentence = exampleSentence.displayText
        var attributed = AttributedString(sentence)

        guard let headword, !headword.isEmpty else { return attributed }

        let stopWords: Set<String> = ["is", "be", "to", "the", "a", "an", "of", "in", "on", "at", "20"]
        let tokens = headword
            .lowercased()
            .split(whereSeparator: { !$0.isLetter })
            .map(String.init)
            .filter { $0.count > 2 && !stopWords.contains($0) }

        let searchTerms = tokens.isEmpty ? [headword.lowercased()] : tokens
        let lowerSentence = sentence.lowercased()

        for term in searchTerms {
            var searchStart = lowerSentence.startIndex
            while let range = lowerSentence.range(of: term, range: searchStart..<lowerSentence.endIndex) {
                if let attrRange = Range(range, in: attributed) {
                    attributed[attrRange].font = DistinctionTheme.exampleEnglishFont.weight(.bold)
                    attributed[attrRange].foregroundColor = .primary
                }
                searchStart = range.upperBound
            }
        }

        return attributed
    }
}
