import SwiftUI

private enum WordListPage: Int, CaseIterable, Identifiable {
    case swipe
    case numbered
    case alphabetical
    case quiz

    var id: Int { rawValue }

    var title: String {
        switch self {
        case .swipe:
            return "単語帳"
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
    @State private var selectedPage = WordListPage.swipe

    private var bookStyle: BookStyle {
        DistinctionTheme.bookStyle(for: book)
    }

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
            bookHeader

            Picker("表示", selection: $selectedPage) {
                ForEach(WordListPage.allCases) { page in
                    Text(page.title).tag(page)
                }
            }
            .pickerStyle(.segmented)
            .padding(.horizontal, 16)
            .padding(.vertical, 10)

            Group {
                switch selectedPage {
                case .swipe:
                    WordSwipeBrowserView(words: filteredWords)
                case .numbered:
                    wordList(words: filteredWords)
                case .alphabetical:
                    wordList(words: alphabeticalWords)
                case .quiz:
                    QuizView(
                        viewModel: dependencyContainer.quizViewModel,
                        showsBookPicker: false
                    )
                    .onAppear {
                        dependencyContainer.quizViewModel.configure(book: book)
                    }
                }
            }
        }
        .background(DistinctionTheme.screenBackground)
        .navigationTitle(book.title)
        .navigationBarTitleDisplayMode(.inline)
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

    private var bookHeader: some View {
        HStack(spacing: 14) {
            BookCoverView(book: book, size: .medium)

            VStack(alignment: .leading, spacing: 4) {
                Text(book.title)
                    .font(.headline)
                Text("\(book.wordCount) 語")
                    .font(.subheadline)
                    .foregroundStyle(.secondary)
            }

            Spacer()
        }
        .padding(.horizontal, 16)
        .padding(.vertical, 12)
        .background(DistinctionTheme.listBackground)
        .overlay(alignment: .bottom) {
            Rectangle()
                .fill(Color(.separator).opacity(0.3))
                .frame(height: 1)
        }
    }

    private func wordList(words: [VocabularyWord]) -> some View {
        List(words) { word in
            NavigationLink(value: word) {
                WordListRow(word: word, accentColor: bookStyle.accentColor)
            }
            .listRowBackground(DistinctionTheme.listBackground)
        }
        .listStyle(.plain)
        .scrollContentBackground(.hidden)
    }
}

private struct WordListRow: View {
    let word: VocabularyWord
    let accentColor: Color

    var body: some View {
        HStack(alignment: .center, spacing: DistinctionTheme.Spacing.md) {
            Text(String(format: "%03d", word.entryNumber))
                .font(.system(size: 12, weight: .bold, design: .rounded).monospacedDigit())
                .foregroundStyle(accentColor)
                .frame(width: 38, height: 24)
                .background(
                    RoundedRectangle(cornerRadius: 6, style: .continuous)
                        .fill(accentColor.opacity(0.12))
                )

            VStack(alignment: .leading, spacing: 3) {
                Text(word.headword)
                    .font(.system(size: 17, weight: .semibold, design: .serif))
                    .foregroundStyle(.primary)

                if let japaneseMeaning = word.displayJapaneseMeaning {
                    Text(japaneseMeaning)
                        .font(.caption)
                        .foregroundStyle(.secondary)
                        .lineLimit(1)
                } else if let nativeDefinition = word.displayNativeDefinition {
                    Text(nativeDefinition)
                        .font(.caption)
                        .foregroundStyle(.secondary)
                        .lineLimit(1)
                }
            }

            Spacer(minLength: 4)
        }
        .padding(.vertical, 6)
    }
}

private struct WordSwipeBrowserView: View {
    let words: [VocabularyWord]
    @State private var currentIndex = 0
    @Environment(AVAudioPlaybackService.self) private var audioPlaybackService

    var body: some View {
        Group {
            if words.isEmpty {
                ContentUnavailableView.search(text: "")
            } else {
                VStack(spacing: 0) {
                    HStack {
                        Text("\(currentIndex + 1) / \(words.count)")
                            .font(.caption.monospacedDigit().weight(.medium))
                            .foregroundStyle(.secondary)
                        Spacer()
                        Text("スワイプで次の単語")
                            .font(.caption)
                            .foregroundStyle(.tertiary)
                    }
                    .padding(.horizontal, 20)
                    .padding(.vertical, 10)

                    TabView(selection: $currentIndex) {
                        ForEach(Array(words.enumerated()), id: \.element.id) { index, word in
                            ScrollView {
                                DistinctionWordPanel(
                                    word: word,
                                    showsDetails: true,
                                    showsExamples: true,
                                    alignment: .leading
                                )
                                .padding(20)
                                .frame(maxWidth: .infinity, alignment: .leading)
                            }
                            .tag(index)
                        }
                    }
                    .tabViewStyle(.page(indexDisplayMode: .never))
                }
            }
        }
        .background(DistinctionTheme.listBackground)
        .onAppear {
            playAudioForCurrentWord()
        }
        .onChange(of: currentIndex) { _, _ in
            playAudioForCurrentWord()
        }
        .onChange(of: words.map(\.id)) { _, _ in
            currentIndex = 0
            playAudioForCurrentWord()
        }
        .onDisappear {
            audioPlaybackService.stop()
        }
    }

    private func playAudioForCurrentWord() {
        guard words.indices.contains(currentIndex) else { return }
        audioPlaybackService.play(resource: words[currentIndex].headwordAudioResource)
    }
}
