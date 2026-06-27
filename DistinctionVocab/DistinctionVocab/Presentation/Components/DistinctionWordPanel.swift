import SwiftUI

struct DistinctionWordPanel: View {
    let word: VocabularyWord
    var showsDetails = true
    var showsExamples = true
    var alignment: HorizontalAlignment = .leading
    @Environment(AVAudioPlaybackService.self) private var audioPlaybackService

    private var frameAlignment: Alignment {
        alignment == .center ? .center : .leading
    }

    private var textAlignment: TextAlignment {
        alignment == .center ? .center : .leading
    }

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
        VStack(alignment: alignment, spacing: DistinctionTheme.Spacing.md) {
            Text(String(format: "%03d", word.entryNumber))
                .font(DistinctionTheme.entryNumberFont)
                .foregroundStyle(DistinctionTheme.accent)
                .padding(.horizontal, 10)
                .padding(.vertical, 4)
                .background(Capsule().fill(DistinctionTheme.accentSoft))
                .frame(maxWidth: .infinity, alignment: frameAlignment)

            Button {
                audioPlaybackService.toggle(resource: word.headwordAudioResource)
            } label: {
                HStack(alignment: .firstTextBaseline, spacing: DistinctionTheme.Spacing.md) {
                    Text(word.headword)
                        .font(DistinctionTheme.headwordFont)
                        .foregroundStyle(.primary)
                        .multilineTextAlignment(textAlignment)
                        .fixedSize(horizontal: false, vertical: true)

                    Image(systemName: headwordIsPlaying ? "speaker.wave.3.fill" : "speaker.wave.2.fill")
                        .font(.title3)
                        .foregroundStyle(headwordIsPlaying ? DistinctionTheme.accent : Color(.tertiaryLabel))
                        .symbolEffect(.variableColor.iterative, isActive: headwordIsPlaying)
                }
                .frame(maxWidth: .infinity, alignment: frameAlignment)
            }
            .buttonStyle(.plain)
        }
        .padding(.bottom, showsDetails ? DistinctionTheme.Spacing.xl : 0)
    }

    private var detailsSection: some View {
        VStack(alignment: alignment, spacing: DistinctionTheme.Spacing.xl) {
            if let phonetic = word.displayPhonetic {
                PhoneticText(phonetic: phonetic, alignment: textAlignment)
                    .frame(maxWidth: .infinity, alignment: frameAlignment)
            }

            if let japaneseMeaning = word.displayJapaneseMeaning {
                VStack(alignment: alignment, spacing: DistinctionTheme.Spacing.sm) {
                    DistinctionSectionLabel(title: "意味", systemImage: "character.book.closed", alignment: alignment)
                    Text(japaneseMeaning)
                        .font(DistinctionTheme.meaningFont)
                        .foregroundStyle(DistinctionTheme.accent)
                        .multilineTextAlignment(textAlignment)
                        .fixedSize(horizontal: false, vertical: true)
                        .frame(maxWidth: .infinity, alignment: frameAlignment)
                }
            }

            if let nativeDefinition = word.displayNativeDefinition {
                VStack(alignment: alignment, spacing: DistinctionTheme.Spacing.sm) {
                    DistinctionSectionLabel(title: "Definition", systemImage: "text.quote", alignment: alignment)
                    Text(nativeDefinition)
                        .font(DistinctionTheme.nativeDefinitionFont)
                        .foregroundStyle(.primary)
                        .multilineTextAlignment(textAlignment)
                        .fixedSize(horizontal: false, vertical: true)
                        .frame(maxWidth: .infinity, alignment: frameAlignment)
                }
            }

            if let etymology = word.displayEtymology {
                VStack(alignment: alignment, spacing: DistinctionTheme.Spacing.sm) {
                    DistinctionSectionLabel(title: "語源", systemImage: "leaf", alignment: alignment)
                    Text(etymology)
                        .font(DistinctionTheme.etymologyFont)
                        .foregroundStyle(.secondary)
                        .multilineTextAlignment(textAlignment)
                        .fixedSize(horizontal: false, vertical: true)
                        .frame(maxWidth: .infinity, alignment: .leading)
                        .padding(DistinctionTheme.Spacing.md)
                        .frame(maxWidth: .infinity, alignment: .leading)
                        .background(
                            RoundedRectangle(cornerRadius: DistinctionTheme.Radius.sm, style: .continuous)
                                .fill(DistinctionTheme.subtleSurface)
                        )
                }
            }
        }
        .padding(.bottom, showsExamples && !word.exampleSentences.isEmpty ? DistinctionTheme.Spacing.xl : 0)
    }

    private var examplesSection: some View {
        VStack(alignment: .leading, spacing: DistinctionTheme.Spacing.md) {
            DistinctionSectionLabel(title: "例文", systemImage: "text.alignleft")

            VStack(alignment: .leading, spacing: 0) {
                ForEach(word.exampleSentences) { exampleSentence in
                    DistinctionExampleRow(
                        exampleSentence: exampleSentence,
                        headword: word.headword
                    )

                    if exampleSentence.id != word.exampleSentences.last?.id {
                        Rectangle()
                            .fill(DistinctionTheme.hairline)
                            .frame(height: 0.5)
                            .padding(.leading, 58)
                    }
                }
            }
            .distinctionCard(background: DistinctionTheme.cardBackground)
        }
    }

    private var headwordIsPlaying: Bool {
        audioPlaybackService.isPlaying
            && audioPlaybackService.currentlyPlayingResourcePath == word.headwordAudioResource.relativePath
    }
}
