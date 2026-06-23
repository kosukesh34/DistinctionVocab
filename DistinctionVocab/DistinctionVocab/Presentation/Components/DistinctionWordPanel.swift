import SwiftUI

struct DistinctionWordPanel: View {
    let word: VocabularyWord
    var showsDetails = true
    var showsExamples = true
    var alignment: HorizontalAlignment = .leading
    @Environment(AVAudioPlaybackService.self) private var audioPlaybackService

    var body: some View {
        VStack(alignment: alignment, spacing: 0) {
            headwordSection

            if showsDetails {
                detailsSection
                    .transition(.opacity.combined(with: .move(edge: .top)))
            }

            if showsDetails, showsExamples, !word.exampleSentences.isEmpty {
                examplesSection
                    .transition(.opacity.combined(with: .move(edge: .bottom)))
            }
        }
        .animation(.easeInOut(duration: 0.2), value: showsDetails)
        .animation(.easeInOut(duration: 0.2), value: showsExamples)
    }

    private var headwordSection: some View {
        VStack(alignment: alignment, spacing: 10) {
            Text(String(format: "%03d", word.entryNumber))
                .font(.caption.monospacedDigit().weight(.semibold))
                .foregroundStyle(.secondary)

            Button {
                audioPlaybackService.toggle(resource: word.headwordAudioResource)
            } label: {
                HStack(alignment: .center, spacing: 10) {
                    Text(word.headword)
                        .font(DistinctionTheme.headwordFont)
                        .foregroundStyle(.primary)
                        .multilineTextAlignment(alignment == .center ? .center : .leading)
                        .fixedSize(horizontal: false, vertical: true)

                    Image(systemName: headwordIsPlaying ? "speaker.wave.3.fill" : "speaker.wave.2")
                        .font(.title3)
                        .foregroundStyle(headwordIsPlaying ? DistinctionTheme.accent : .secondary)
                }
                .frame(maxWidth: .infinity, alignment: alignment == .center ? .center : .leading)
            }
            .buttonStyle(.plain)
        }
        .padding(.bottom, showsDetails ? 16 : 0)
    }

    private var detailsSection: some View {
        VStack(alignment: alignment, spacing: 10) {
            if let phonetic = word.displayPhonetic {
                PhoneticText(phonetic: phonetic)
                    .frame(maxWidth: .infinity, alignment: alignment == .center ? .center : .leading)
            }

            if let japaneseMeaning = word.displayJapaneseMeaning {
                Text(japaneseMeaning)
                    .font(DistinctionTheme.meaningFont)
                    .foregroundStyle(.primary)
                    .multilineTextAlignment(alignment == .center ? .center : .leading)
                    .fixedSize(horizontal: false, vertical: true)
                    .frame(maxWidth: .infinity, alignment: alignment == .center ? .center : .leading)
            }
        }
        .padding(.bottom, showsExamples && !word.exampleSentences.isEmpty ? 12 : 0)
    }

    private var examplesSection: some View {
        VStack(alignment: .leading, spacing: 0) {
            Divider()
                .padding(.bottom, 8)

            ForEach(word.exampleSentences) { exampleSentence in
                DistinctionExampleRow(exampleSentence: exampleSentence)

                if exampleSentence.id != word.exampleSentences.last?.id {
                    Divider()
                        .padding(.leading, 40)
                }
            }
        }
    }

    private var headwordIsPlaying: Bool {
        audioPlaybackService.isPlaying
            && audioPlaybackService.currentlyPlayingResourcePath == word.headwordAudioResource.relativePath
    }
}
