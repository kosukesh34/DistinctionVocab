import SwiftUI

enum DistinctionTheme {
    // Official Distinction App brand accent (from AccentColor asset)
    static let accent = Color(red: 0.35, green: 0.40, blue: 0.82)
    static let accentSoft = Color(red: 0.35, green: 0.40, blue: 0.82).opacity(0.12)

    // Study ratings — Distinction uses Hard(赤)/Good(藍)/Easy(緑)
    static let easy = Color(red: 0.18, green: 0.72, blue: 0.45)
    static let good = Color(red: 0.35, green: 0.40, blue: 0.82)
    static let hard = Color(red: 0.90, green: 0.36, blue: 0.32)

    static let cardBackground = Color(.secondarySystemGroupedBackground)
    static let screenBackground = Color(.systemGroupedBackground)
    static let listBackground = Color(.systemBackground)
    static let subtleSurface = Color(.secondarySystemBackground)
    static let hairline = Color(.separator).opacity(0.4)

    // MARK: - Design tokens

    enum Spacing {
        static let xs: CGFloat = 4
        static let sm: CGFloat = 8
        static let md: CGFloat = 12
        static let lg: CGFloat = 16
        static let xl: CGFloat = 20
        static let xxl: CGFloat = 28
    }

    enum Radius {
        static let sm: CGFloat = 10
        static let md: CGFloat = 14
        static let lg: CGFloat = 18
        static let xl: CGFloat = 24
    }

    static let cardShadow = Color.black.opacity(0.05)

    // MARK: - Typography

    static let headwordFont = Font.system(size: 34, weight: .bold, design: .serif)
    static let nativeDefinitionFont = Font.system(size: 18, weight: .regular, design: .serif)
    static let meaningFont = Font.system(size: 22, weight: .semibold)
    static let etymologyFont = Font.system(size: 15, weight: .regular)
    static let exampleEnglishFont = Font.system(size: 17, weight: .regular)
    static let exampleJapaneseFont = Font.system(size: 15, weight: .regular)
    static let entryNumberFont = Font.system(size: 13, weight: .semibold, design: .rounded)
    static let sectionTitleFont = Font.system(size: 12, weight: .semibold)
    static let bookTitleFont = Font.system(size: 17, weight: .semibold)

    static func bookStyle(for book: VocabularyBook) -> BookStyle {
        BookStyle.style(for: book)
    }
}

// MARK: - Reusable section label (Distinction-style minimal uppercase caption)

struct DistinctionSectionLabel: View {
    let title: String
    var systemImage: String?
    var alignment: HorizontalAlignment = .leading

    var body: some View {
        Label {
            Text(title)
                .tracking(0.8)
        } icon: {
            if let systemImage {
                Image(systemName: systemImage)
            }
        }
        .labelStyle(.titleAndIcon)
        .font(DistinctionTheme.sectionTitleFont)
        .foregroundStyle(.secondary)
        .textCase(.uppercase)
        .frame(maxWidth: .infinity, alignment: alignment == .center ? .center : .leading)
    }
}

// MARK: - Card container modifier

extension View {
    func distinctionCard(
        cornerRadius: CGFloat = DistinctionTheme.Radius.lg,
        padding: CGFloat? = nil,
        background: Color = DistinctionTheme.listBackground
    ) -> some View {
        self
            .padding(padding ?? 0)
            .background(
                RoundedRectangle(cornerRadius: cornerRadius, style: .continuous)
                    .fill(background)
            )
            .overlay(
                RoundedRectangle(cornerRadius: cornerRadius, style: .continuous)
                    .stroke(DistinctionTheme.hairline, lineWidth: 0.5)
            )
    }
}

struct BookStyle {
    let gradientColors: [Color]
    let romanNumeral: String
    let accentColor: Color

    static func style(for book: VocabularyBook) -> BookStyle {
        switch book.identifier {
        case "dist1":
            return BookStyle(
                gradientColors: [Color(red: 0.75, green: 0.22, blue: 0.17), Color(red: 0.91, green: 0.30, blue: 0.24)],
                romanNumeral: "I",
                accentColor: Color(red: 0.91, green: 0.30, blue: 0.24)
            )
        case "dist2":
            return BookStyle(
                gradientColors: [Color(red: 0.16, green: 0.50, blue: 0.73), Color(red: 0.20, green: 0.60, blue: 0.86)],
                romanNumeral: "II",
                accentColor: Color(red: 0.20, green: 0.60, blue: 0.86)
            )
        case "dist3":
            return BookStyle(
                gradientColors: [Color(red: 0.09, green: 0.63, blue: 0.52), Color(red: 0.10, green: 0.74, blue: 0.61)],
                romanNumeral: "III",
                accentColor: Color(red: 0.10, green: 0.74, blue: 0.61)
            )
        case "dist4":
            return BookStyle(
                gradientColors: [Color(red: 0.56, green: 0.27, blue: 0.68), Color(red: 0.61, green: 0.35, blue: 0.71)],
                romanNumeral: "IV",
                accentColor: Color(red: 0.61, green: 0.35, blue: 0.71)
            )
        case "dist5":
            return BookStyle(
                gradientColors: [Color(red: 0.83, green: 0.33, blue: 0.00), Color(red: 0.90, green: 0.49, blue: 0.13)],
                romanNumeral: "V",
                accentColor: Color(red: 0.90, green: 0.49, blue: 0.13)
            )
        case "dist6":
            return BookStyle(
                gradientColors: [Color(red: 0.17, green: 0.24, blue: 0.31), Color(red: 0.20, green: 0.29, blue: 0.37)],
                romanNumeral: "VI",
                accentColor: Color(red: 0.20, green: 0.29, blue: 0.37)
            )
        case "reibun":
            return BookStyle(
                gradientColors: [Color(red: 0.45, green: 0.28, blue: 0.62), Color(red: 0.58, green: 0.38, blue: 0.74)],
                romanNumeral: "例",
                accentColor: Color(red: 0.58, green: 0.38, blue: 0.74)
            )
        default:
            return BookStyle(
                gradientColors: [DistinctionTheme.accent, DistinctionTheme.accent.opacity(0.7)],
                romanNumeral: "?",
                accentColor: DistinctionTheme.accent
            )
        }
    }
}
