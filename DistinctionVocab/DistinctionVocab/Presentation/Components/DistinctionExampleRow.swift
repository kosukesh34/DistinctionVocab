import SwiftUI

struct DistinctionExampleRow: View {
    let exampleSentence: ExampleSentence
    @Environment(AVAudioPlaybackService.self) private var audioPlaybackService

    private var isPlaying: Bool {
        audioPlaybackService.isPlaying
            && audioPlaybackService.currentlyPlayingResourcePath == exampleSentence.audioResource.relativePath
    }

    var body: some View {
        Button {
            audioPlaybackService.toggle(resource: exampleSentence.audioResource)
        } label: {
            HStack(alignment: .top, spacing: 12) {
                Text(exampleSentence.label)
                    .font(.caption.weight(.bold))
                    .foregroundStyle(DistinctionTheme.accent)
                    .frame(width: 28, height: 28)
                    .background(
                        Circle()
                            .fill(DistinctionTheme.accent.opacity(0.12))
                    )

                VStack(alignment: .leading, spacing: 6) {
                    Text(exampleSentence.displayText)
                        .font(DistinctionTheme.exampleEnglishFont)
                        .foregroundStyle(.primary)
                        .multilineTextAlignment(.leading)
                        .fixedSize(horizontal: false, vertical: true)

                    if let japaneseTranslation = exampleSentence.displayJapaneseTranslation {
                        Text(japaneseTranslation)
                            .font(DistinctionTheme.exampleJapaneseFont)
                            .foregroundStyle(.secondary)
                            .multilineTextAlignment(.leading)
                            .fixedSize(horizontal: false, vertical: true)
                    }
                }

                Spacer(minLength: 8)

                Image(systemName: isPlaying ? "speaker.wave.3.fill" : "speaker.wave.2")
                    .font(.body)
                    .foregroundStyle(isPlaying ? DistinctionTheme.accent : .secondary)
                    .frame(width: 24)
            }
            .contentShape(Rectangle())
        }
        .buttonStyle(.plain)
        .padding(.vertical, 10)
    }
}
