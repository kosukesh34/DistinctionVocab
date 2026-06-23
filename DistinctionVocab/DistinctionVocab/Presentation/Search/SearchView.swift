import SwiftUI

struct SearchView: View {
    @Bindable var viewModel: SearchViewModel
    let dependencyContainer: DependencyContainer
    @State private var searchQuery = ""

    var body: some View {
        NavigationStack {
            Group {
                if searchQuery.trimmingCharacters(in: .whitespacesAndNewlines).isEmpty {
                    ContentUnavailableView(
                        "単語を検索",
                        systemImage: "magnifyingglass",
                        description: Text("見出し語から横断検索できます")
                    )
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
                            VStack(alignment: .leading, spacing: 4) {
                                Text(searchResult.word.headword)
                                    .font(.body)
                                Text(searchResult.book.title)
                                    .font(.caption)
                                    .foregroundStyle(.secondary)
                            }
                        }
                    }
                    .listStyle(.plain)
                }
            }
            .navigationTitle("検索")
            .searchable(text: $searchQuery, prompt: "見出し語を入力")
            .onChange(of: searchQuery) { _, updatedQuery in
                viewModel.updateSearchQuery(updatedQuery)
            }
        }
    }
}
