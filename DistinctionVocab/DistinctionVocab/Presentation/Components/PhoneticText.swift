import SwiftUI

struct PhoneticText: View {
    let phonetic: String
    var alignment: TextAlignment = .leading

    var body: some View {
        Text("/\(phonetic)/")
            .font(.system(size: 16, design: .serif))
            .italic()
            .foregroundStyle(Color(.tertiaryLabel))
            .multilineTextAlignment(alignment)
    }
}
