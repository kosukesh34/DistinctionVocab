import SwiftUI

@main
struct DistinctionVocabApp: App {
    private let dependencyContainer = DependencyContainer()

    var body: some Scene {
        WindowGroup {
            ContentView(dependencyContainer: dependencyContainer)
                .task {
                    dependencyContainer.vocabularyCatalogViewModel.loadCatalogIfNeeded()
                }
        }
    }
}
