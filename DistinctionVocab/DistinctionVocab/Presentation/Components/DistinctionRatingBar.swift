import SwiftUI

struct DistinctionRatingBar: View {
    let onRate: (StudyRating) -> Void

    var body: some View {
        VStack(spacing: DistinctionTheme.Spacing.sm) {
            Text("どのくらい覚えていましたか？")
                .font(.caption)
                .foregroundStyle(.secondary)

            HStack(spacing: DistinctionTheme.Spacing.md) {
                ratingButton(.hard, color: DistinctionTheme.hard, icon: "arrow.counterclockwise", subtitle: "もう一度")
                ratingButton(.good, color: DistinctionTheme.good, icon: "checkmark", subtitle: "普通")
                ratingButton(.easy, color: DistinctionTheme.easy, icon: "hand.thumbsup.fill", subtitle: "簡単")
            }
        }
        .padding(.horizontal, DistinctionTheme.Spacing.lg)
        .padding(.top, DistinctionTheme.Spacing.md)
        .padding(.bottom, DistinctionTheme.Spacing.sm)
        .background(
            Rectangle()
                .fill(.bar)
                .shadow(color: DistinctionTheme.cardShadow, radius: 8, y: -2)
                .ignoresSafeArea(edges: .bottom)
        )
    }

    private func ratingButton(
        _ rating: StudyRating,
        color: Color,
        icon: String,
        subtitle: String
    ) -> some View {
        Button {
            onRate(rating)
        } label: {
            VStack(spacing: 3) {
                HStack(spacing: 6) {
                    Image(systemName: icon)
                        .font(.system(size: 14, weight: .bold))
                    Text(rating.title)
                        .font(.system(size: 16, weight: .semibold))
                }
                .foregroundStyle(.white)

                Text(subtitle)
                    .font(.system(size: 11, weight: .medium))
                    .foregroundStyle(.white.opacity(0.85))
            }
            .frame(maxWidth: .infinity)
            .padding(.vertical, DistinctionTheme.Spacing.md)
            .background(
                RoundedRectangle(cornerRadius: DistinctionTheme.Radius.md, style: .continuous)
                    .fill(color)
                    .shadow(color: color.opacity(0.3), radius: 4, y: 2)
            )
        }
        .buttonStyle(.plain)
    }
}
