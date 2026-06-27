import SwiftUI

struct SearchView: View {
    @Bindable var viewModel: SearchViewModel
    let dependencyContainer: DependencyContainer
    @State private var searchQuery = ""

    var body: some View {
        NavigationStack {
            Group {
                if searchQuery.trimmingCharacters(in: .whitespacesAndNewlines).isEmpty {
                    emptyStateView
                } else if viewModel.searchResults.isEmpty {
                    ContentUnavailableView.search(text: searchQuery)
                } else {
                    List(viewModel.searchResults) { searchResult in
                        NavigationLink {
                            WordDetailView(
                                viewModel: dependencyContainer.makeWordDetailViewModel(
                                    word: searchResult.word,
                                    bookTitle: searchResult.book.title
                                )
                            )
                        } label: {
                            SearchResultRow(searchResult: searchResult)
                        }
                        .listRowBackground(DistinctionTheme.listBackground)
                    }
                    .listStyle(.plain)
                    .scrollContentBackground(.hidden)
                }
            }
            .background(DistinctionTheme.screenBackground)
            .navigationTitle("検索")
            .searchable(text: $searchQuery, prompt: "見出し語・例文を検索")
            .onChange(of: searchQuery) { _, updatedQuery in
                viewModel.updateSearchQuery(updatedQuery)
            }
        }
    }

    private var emptyStateView: some View {
        VStack(spacing: 16) {
            Image(systemName: "magnifyingglass")
                .font(.system(size: 48))
                .foregroundStyle(DistinctionTheme.accent.opacity(0.5))

            Text("単語を検索")
                .font(.title3.bold())

            Text("見出し語から横断検索できます")
                .font(.subheadline)
                .foregroundStyle(.secondary)
        }
        .frame(maxWidth: .infinity, maxHeight: .infinity)
    }
}

private struct SearchResultRow: View {
    let searchResult: VocabularySearchResult

    private var bookStyle: BookStyle {
        DistinctionTheme.bookStyle(for: searchResult.book)
    }

    var body: some View {
        HStack(spacing: 14) {
            BookCoverView(book: searchResult.book, size: .small)

            VStack(alignment: .leading, spacing: 4) {
                Text(searchResult.word.headword)
                    .font(.system(size: 17, weight: .semibold, design: .serif))

                Text(searchResult.book.title)
                    .font(.caption)
                    .foregroundStyle(bookStyle.accentColor)

                if let meaning = searchResult.word.displayJapaneseMeaning {
                    Text(meaning)
                        .font(.caption)
                        .foregroundStyle(.secondary)
                        .lineLimit(1)
                }
            }
        }
        .padding(.vertical, 4)
    }
}
