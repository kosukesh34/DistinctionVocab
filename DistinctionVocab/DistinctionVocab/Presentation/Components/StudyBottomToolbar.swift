import SwiftUI

struct StudyBottomToolbar: View {
    @Binding var areDetailsVisible: Bool
    @Binding var isBookmarked: Bool
    let onPlayAll: () -> Void
    var isPlayingAll = false

    var body: some View {
        HStack(spacing: 0) {
            toolbarButton(
                icon: areDetailsVisible ? "eye.fill" : "eye.slash.fill",
                label: "表示",
                isActive: areDetailsVisible
            ) {
                areDetailsVisible.toggle()
            }

            Divider()
                .frame(height: 28)

            toolbarButton(
                icon: isBookmarked ? "bookmark.fill" : "bookmark",
                label: "ブックマーク",
                isActive: isBookmarked
            ) {
                isBookmarked.toggle()
            }

            Divider()
                .frame(height: 28)

            toolbarButton(
                icon: isPlayingAll ? "stop.fill" : "play.fill",
                label: "再生",
                isActive: isPlayingAll
            ) {
                onPlayAll()
            }
        }
        .frame(maxWidth: .infinity)
        .padding(.vertical, 10)
        .background(
            Rectangle()
                .fill(.bar)
                .shadow(color: .black.opacity(0.06), radius: 8, y: -2)
        )
    }

    private func toolbarButton(
        icon: String,
        label: String,
        isActive: Bool,
        action: @escaping () -> Void
    ) -> some View {
        Button(action: action) {
            VStack(spacing: 4) {
                Image(systemName: icon)
                    .font(.system(size: 20))
                    .foregroundStyle(isActive ? DistinctionTheme.accent : .secondary)
                Text(label)
                    .font(.system(size: 10))
                    .foregroundStyle(.secondary)
            }
            .frame(maxWidth: .infinity)
        }
        .buttonStyle(.plain)
    }
}
