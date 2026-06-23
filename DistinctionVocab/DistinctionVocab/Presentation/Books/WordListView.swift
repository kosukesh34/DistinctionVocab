import SwiftUI

private enum WordListPage: Int, CaseIterable, Identifiable {
    case numbered
    case alphabetical
    case quiz

    var id: Int { rawValue }

    var title: String {
        switch self {
        case .numbered:
            return "番号順"
        case .alphabetical:
            return "あいうえお順"
        case .quiz:
            return "テスト"
        }
    }
}

struct WordListView: View {
    let book: VocabularyBook
    let dependencyContainer: DependencyContainer
    @State private var searchQuery = ""
    @State private var selectedPage = WordListPage.numbered

    private var filteredWords: [VocabularyWord] {
        guard !searchQuery.isEmpty else { return book.words }
        return book.words.filter {
            $0.headword.localizedCaseInsensitiveContains(searchQuery)
        }
    }

    private var alphabeticalWords: [VocabularyWord] {
        filteredWords.sorted {
            $0.headword.localizedCaseInsensitiveCompare($1.headword) == .orderedAscending
        }
    }

    var body: some View {
        VStack(spacing: 0) {
            Picker("表示", selection: $selectedPage) {
                ForEach(WordListPage.allCases) { page in
                    Text(page.title).tag(page)
                }
            }
            .pickerStyle(.segmented)
            .padding(.horizontal)
            .padding(.vertical, 8)

            TabView(selection: $selectedPage) {
                wordList(words: filteredWords)
                    .tag(WordListPage.numbered)

                wordList(words: alphabeticalWords)
                    .tag(WordListPage.alphabetical)

                QuizView(
                    viewModel: dependencyContainer.quizViewModel,
                    showsBookPicker: false
                )
                .tag(WordListPage.quiz)
                .onAppear {
                    dependencyContainer.quizViewModel.configure(book: book)
                }
            }
            .tabViewStyle(.page(indexDisplayMode: .never))
        }
        .navigationTitle(book.title)
        .navigationBarTitleDisplayMode(.large)
        .searchable(text: $searchQuery, prompt: "単語を検索")
        .navigationDestination(for: VocabularyWord.self) { word in
            WordDetailView(
                viewModel: dependencyContainer.makeWordDetailViewModel(
                    word: word,
                    bookTitle: book.title
                )
            )
        }
    }

    private func wordList(words: [VocabularyWord]) -> some View {
        List(words) { word in
            NavigationLink(value: word) {
                WordListRow(word: word)
            }
        }
        .listStyle(.plain)
    }
}

private struct WordListRow: View {
    let word: VocabularyWord

    var body: some View {
        HStack(alignment: .top, spacing: 12) {
            Text(String(format: "%03d", word.entryNumber))
                .font(.caption.monospacedDigit())
                .foregroundStyle(.secondary)
                .frame(width: 36, alignment: .leading)

            VStack(alignment: .leading, spacing: 4) {
                Text(word.headword)
                    .font(.body)

                if let phonetic = word.displayPhonetic {
                    PhoneticText(phonetic: phonetic)
                        .font(.caption)
                }

                if let japaneseMeaning = word.displayJapaneseMeaning {
                    Text(japaneseMeaning)
                        .font(.caption)
                        .foregroundStyle(.secondary)
                        .lineLimit(1)
                }
            }
        }
        .padding(.vertical, 2)
    }
}
