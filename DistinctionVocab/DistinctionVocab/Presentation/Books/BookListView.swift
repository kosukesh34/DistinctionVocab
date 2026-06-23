import SwiftUI

struct BookListView: View {
    @Bindable var viewModel: VocabularyCatalogViewModel
    let dependencyContainer: DependencyContainer

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
                    List(viewModel.availableBooks) { book in
                        NavigationLink(value: book) {
                            BookRowView(book: book)
                        }
                    }
                    .listStyle(.insetGrouped)
                }
            }
            .navigationTitle("ブック")
            .navigationDestination(for: VocabularyBook.self) { book in
                WordListView(book: book, dependencyContainer: dependencyContainer)
            }
        }
    }
}

private struct BookRowView: View {
    let book: VocabularyBook

    var body: some View {
        HStack(spacing: 16) {
            ZStack {
                RoundedRectangle(cornerRadius: 12, style: .continuous)
                    .fill(
                        LinearGradient(
                            colors: [
                                Color.accentColor.opacity(0.8),
                                Color.accentColor.opacity(0.4)
                            ],
                            startPoint: .topLeading,
                            endPoint: .bottomTrailing
                        )
                    )
                    .frame(width: 52, height: 52)
                Text("\(book.words.first?.entryNumber ?? 1)")
                    .font(.headline.bold())
                    .foregroundStyle(.white)
            }

            VStack(alignment: .leading, spacing: 4) {
                Text(book.title)
                    .font(.headline)
                Text("\(book.wordCount) 語")
                    .font(.subheadline)
                    .foregroundStyle(.secondary)
            }
        }
        .padding(.vertical, 4)
    }
}
