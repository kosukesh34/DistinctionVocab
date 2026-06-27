import SwiftUI

struct BookListView: View {
    @Bindable var viewModel: VocabularyCatalogViewModel
    let dependencyContainer: DependencyContainer

    private let columns = [
        GridItem(.flexible(), spacing: 16),
        GridItem(.flexible(), spacing: 16)
    ]

    var body: some View {
        NavigationStack {
            Group {
                if let errorMessage = viewModel.loadingErrorMessage {
                    ContentUnavailableView(
                        "読み込みエラー",
                        systemImage: "exclamationmark.triangle",
                        description: Text(errorMessage)
                    )
                } else if viewModel.availableBooks.isEmpty {
                    ProgressView("読み込み中…")
                } else {
                    ScrollView {
                        LazyVGrid(columns: columns, spacing: 16) {
                            ForEach(viewModel.availableBooks) { book in
                                NavigationLink(value: book) {
                                    DiscoverBookCard(book: book)
                                }
                                .buttonStyle(.plain)
                            }
                        }
                        .padding(16)
                    }
                }
            }
            .background(DistinctionTheme.screenBackground)
            .navigationTitle("見つける")
            .navigationDestination(for: VocabularyBook.self) { book in
                WordListView(book: book, dependencyContainer: dependencyContainer)
            }
        }
    }
}

private struct DiscoverBookCard: View {
    let book: VocabularyBook

    var body: some View {
        VStack(alignment: .leading, spacing: DistinctionTheme.Spacing.md) {
            BookCoverView(book: book, size: .flexible)
                .frame(maxWidth: .infinity)

            VStack(alignment: .leading, spacing: DistinctionTheme.Spacing.xs) {
                Text(book.title)
                    .font(DistinctionTheme.bookTitleFont)
                    .foregroundStyle(.primary)
                    .lineLimit(1)

                Text("\(book.wordCount) 語")
                    .font(.caption)
                    .foregroundStyle(.secondary)
            }
        }
        .padding(DistinctionTheme.Spacing.lg)
        .frame(maxWidth: .infinity, alignment: .leading)
        .distinctionCard()
    }
}