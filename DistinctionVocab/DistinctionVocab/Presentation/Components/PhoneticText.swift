import SwiftUI

struct PhoneticText: View {
    let phonetic: String

    var body: some View {
        Text("/\(phonetic)/")
            .font(.system(.subheadline, design: .serif))
            .foregroundStyle(.tertiary)
            .multilineTextAlignment(.center)
    }
}
