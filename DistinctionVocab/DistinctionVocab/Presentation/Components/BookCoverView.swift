import SwiftUI

struct BookCoverView: View {
    let book: VocabularyBook
    var size: BookCoverSize = .medium

    private var style: BookStyle {
        DistinctionTheme.bookStyle(for: book)
    }

    var body: some View {
        ZStack(alignment: .bottomLeading) {
            RoundedRectangle(cornerRadius: size.cornerRadius, style: .continuous)
                .fill(
                    LinearGradient(
                        colors: style.gradientColors,
                        startPoint: .topLeading,
                        endPoint: .bottomTrailing
                    )
                )

            VStack(alignment: .leading, spacing: size.titleSpacing) {
                Text(style.romanNumeral)
                    .font(size.numeralFont)
                    .foregroundStyle(.white.opacity(0.95))

                if size.showsTitle {
                    Text(book.title)
                        .font(size.titleFont)
                        .foregroundStyle(.white.opacity(0.9))
                        .lineLimit(2)
                        .minimumScaleFactor(0.8)
                }
            }
            .padding(size.contentPadding)
        }
        .aspectRatio(size.aspectRatio, contentMode: .fit)
        .frame(maxWidth: size.maxWidth)
        .frame(width: size.fixedWidth, height: size.fixedHeight)
        .shadow(color: style.accentColor.opacity(0.25), radius: size.shadowRadius, y: size.shadowY)
    }
}

enum BookCoverSize {
    case small
    case medium
    case large
    case flexible

    var fixedWidth: CGFloat? {
        switch self {
        case .small: return 48
        case .medium: return 64
        case .large: return 80
        case .flexible: return nil
        }
    }

    var fixedHeight: CGFloat? {
        switch self {
        case .small: return 64
        case .medium: return 84
        case .large: return 104
        case .flexible: return nil
        }
    }

    var maxWidth: CGFloat? {
        switch self {
        case .flexible: return .infinity
        default: return nil
        }
    }

    var aspectRatio: CGFloat {
        3.0 / 4.0
    }

    var cornerRadius: CGFloat {
        switch self {
        case .small: return 8
        case .medium: return 10
        case .large, .flexible: return 12
        }
    }

    var numeralFont: Font {
        switch self {
        case .small: return .system(size: 20, weight: .bold, design: .serif)
        case .medium: return .system(size: 26, weight: .bold, design: .serif)
        case .large, .flexible: return .system(size: 32, weight: .bold, design: .serif)
        }
    }

    var titleFont: Font {
        switch self {
        case .small: return .system(size: 8, weight: .semibold)
        case .medium: return .system(size: 10, weight: .semibold)
        case .large, .flexible: return .system(size: 11, weight: .semibold)
        }
    }

    var contentPadding: CGFloat {
        switch self {
        case .small: return 6
        case .medium: return 8
        case .large, .flexible: return 10
        }
    }

    var titleSpacing: CGFloat {
        switch self {
        case .small: return 2
        case .medium: return 4
        case .large, .flexible: return 4
        }
    }

    var shadowRadius: CGFloat {
        switch self {
        case .small: return 4
        case .medium: return 6
        case .large, .flexible: return 8
        }
    }

    var shadowY: CGFloat {
        switch self {
        case .small: return 2
        case .medium: return 3
        case .large, .flexible: return 4
        }
    }

    var showsTitle: Bool {
        self != .small
    }
}
