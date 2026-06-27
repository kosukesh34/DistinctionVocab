import SwiftUI

struct ContentView: View {
    let dependencyContainer: DependencyContainer
    @State private var selectedTabIndex = 0

    var body: some View {
        TabView(selection: $selectedTabIndex) {
            TodayView(
                studyViewModel: dependencyContainer.studyViewModel,
                vocabularyCatalogViewModel: dependencyContainer.vocabularyCatalogViewModel,
                dependencyContainer: dependencyContainer
            )
            .tabItem {
                Label("Today", systemImage: "sun.max.fill")
            }
            .tag(0)

            BookListView(
                viewModel: dependencyContainer.vocabularyCatalogViewModel,
                dependencyContainer: dependencyContainer
            )
            .tabItem {
                Label("見つける", systemImage: "text.book.closed.fill")
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
