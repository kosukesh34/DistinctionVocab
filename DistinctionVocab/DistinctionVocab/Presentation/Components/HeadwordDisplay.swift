import SwiftUI

struct HeadwordDisplay: View {
    let word: VocabularyWord
    var headwordFont: Font = .system(.title, design: .serif, weight: .bold)
    var meaningFont: Font = .title3
    var showsEntryNumber = true
    var alignment: HorizontalAlignment = .center

    var body: some View {
        VStack(alignment: alignment, spacing: 8) {
            if showsEntryNumber {
                Text("#\(word.entryNumber)")
                    .font(.caption.monospacedDigit())
                    .foregroundStyle(.secondary)
            }

            Text(word.headword)
                .font(headwordFont)
                .multilineTextAlignment(alignment == .center ? .center : .leading)
                .fixedSize(horizontal: false, vertical: true)

            if let phonetic = word.displayPhonetic {
                PhoneticText(phonetic: phonetic)
            }

            if let japaneseMeaning = word.displayJapaneseMeaning {
                Text(japaneseMeaning)
                    .font(meaningFont)
                    .foregroundStyle(.secondary)
                    .multilineTextAlignment(alignment == .center ? .center : .leading)
                    .fixedSize(horizontal: false, vertical: true)
            }
        }
    }
}
