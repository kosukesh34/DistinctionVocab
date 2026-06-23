import SwiftUI

struct ContentView: View {
    let dependencyContainer: DependencyContainer
    @State private var selectedTabIndex = 0

    var body: some View {
        TabView(selection: $selectedTabIndex) {
            StudyView(
                viewModel: dependencyContainer.studyViewModel,
                vocabularyCatalogViewModel: dependencyContainer.vocabularyCatalogViewModel,
                quizViewModel: dependencyContainer.quizViewModel
            )
            .tabItem {
                Label("学習", systemImage: "brain.head.profile")
            }
            .tag(0)

            BookListView(
                viewModel: dependencyContainer.vocabularyCatalogViewModel,
                dependencyContainer: dependencyContainer
            )
            .tabItem {
                Label("ブック", systemImage: "books.vertical")
            }
            .tag(1)

            SearchView(
                viewModel: dependencyContainer.searchViewModel,
                dependencyContainer: dependencyContainer
            )
            .tabItem {
                Label("検索", systemImage: "magnifyingglass")
            }
            .tag(2)
        }
        .tint(DistinctionTheme.accent)
        .environment(dependencyContainer.audioPlaybackService)
    }
}

#Preview {
    ContentView(dependencyContainer: DependencyContainer())
}
