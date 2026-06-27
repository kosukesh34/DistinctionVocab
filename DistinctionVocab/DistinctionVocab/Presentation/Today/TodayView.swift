import SwiftUI

struct TodayView: View {
    @Bindable var studyViewModel: StudyViewModel
    @Bindable var vocabularyCatalogViewModel: VocabularyCatalogViewModel
    let dependencyContainer: DependencyContainer
    @State private var showsSettings = false
    @State private var navigationPath = NavigationPath()

    var body: some View {
        NavigationStack(path: $navigationPath) {
            ScrollView {
                VStack(alignment: .leading, spacing: DistinctionTheme.Spacing.xxl) {
                    dailySummaryCard

                    VStack(alignment: .leading, spacing: DistinctionTheme.Spacing.md) {
                        DistinctionSectionLabel(title: "ブックを選んで学習")
                            .padding(.horizontal, DistinctionTheme.Spacing.xl)

                        if vocabularyCatalogViewModel.availableBooks.isEmpty {
                            ProgressView()
                                .frame(maxWidth: .infinity)
                                .padding(.vertical, 40)
                        } else {
                            VStack(spacing: 0) {
                                ForEach(vocabularyCatalogViewModel.availableBooks) { book in
                                    TodayBookRow(book: book) {
                                        startStudy(with: book)
                                    }

                                    if book.id != vocabularyCatalogViewModel.availableBooks.last?.id {
                                        Divider()
                                            .padding(.leading, 92)
                                    }
                                }
                            }
                            .distinctionCard()
                            .padding(.horizontal, DistinctionTheme.Spacing.lg)
                        }
                    }
                }
                .padding(.vertical, DistinctionTheme.Spacing.sm)
            }
            .background(DistinctionTheme.screenBackground)
            .navigationTitle("Today")
            .navigationBarTitleDisplayMode(.large)
            .toolbar {
                ToolbarItem(placement: .topBarTrailing) {
                    Button {
                        showsSettings = true
                    } label: {
                        Image(systemName: "gearshape")
                            .foregroundStyle(DistinctionTheme.accent)
                    }
                }
            }
            .sheet(isPresented: $showsSettings) {
                StudySettingsSheet(
                    studyViewModel: studyViewModel,
                    availableBooks: vocabularyCatalogViewModel.availableBooks
                )
            }
            .navigationDestination(for: TodayDestination.self) { destination in
                switch destination {
                case .study:
                    StudySessionView(
                        viewModel: studyViewModel,
                        vocabularyCatalogViewModel: vocabularyCatalogViewModel
                    )
                }
            }
        }
    }

    private var remainingWords: Int {
        max(0, studyViewModel.dailyWordGoal - studyViewModel.reviewedWordCount)
    }

    private var isGoalComplete: Bool {
        remainingWords == 0 && studyViewModel.reviewedWordCount > 0
    }

    private var recommendedBook: VocabularyBook? {
        studyViewModel.selectedBook ?? vocabularyCatalogViewModel.availableBooks.first
    }

    private var dailySummaryCard: some View {
        VStack(spacing: DistinctionTheme.Spacing.xl) {
            HStack(spacing: DistinctionTheme.Spacing.xl) {
                progressRing

                VStack(alignment: .leading, spacing: 6) {
                    Text(isGoalComplete ? "今日の目標達成！" : "今日の目標")
                        .font(.headline)

                    Text(isGoalComplete ? "お疲れさまでした" : "あと \(remainingWords) 語")
                        .font(.subheadline)
                        .foregroundStyle(.secondary)

                    if let book = recommendedBook {
                        HStack(spacing: 6) {
                            BookCoverView(book: book, size: .small)
                            Text(book.title)
                                .font(.caption)
                                .foregroundStyle(.secondary)
                                .lineLimit(1)
                        }
                        .padding(.top, 2)
                    }
                }

                Spacer()
            }

            if let book = recommendedBook {
                Button {
                    startStudy(with: book)
                } label: {
                    HStack(spacing: 8) {
                        Image(systemName: "play.fill")
                        Text(studyViewModel.reviewedWordCount > 0 ? "学習を続ける" : "今日の学習を始める")
                    }
                    .font(.headline)
                    .foregroundStyle(.white)
                    .frame(maxWidth: .infinity)
                    .padding(.vertical, DistinctionTheme.Spacing.lg)
                    .background(
                        RoundedRectangle(cornerRadius: DistinctionTheme.Radius.md, style: .continuous)
                            .fill(DistinctionTheme.accent)
                            .shadow(color: DistinctionTheme.accent.opacity(0.3), radius: 6, y: 3)
                    )
                }
                .buttonStyle(.plain)
            }
        }
        .padding(DistinctionTheme.Spacing.xl)
        .distinctionCard()
        .padding(.horizontal, DistinctionTheme.Spacing.lg)
    }

    private var progressRing: some View {
        ZStack {
            Circle()
                .stroke(Color(.systemGray5), lineWidth: 7)
                .frame(width: 72, height: 72)

            Circle()
                .trim(from: 0, to: studyProgress)
                .stroke(
                    isGoalComplete ? DistinctionTheme.easy : DistinctionTheme.accent,
                    style: StrokeStyle(lineWidth: 7, lineCap: .round)
                )
                .frame(width: 72, height: 72)
                .rotationEffect(.degrees(-90))
                .animation(.easeInOut, value: studyProgress)

            if isGoalComplete {
                Image(systemName: "checkmark")
                    .font(.system(size: 24, weight: .bold))
                    .foregroundStyle(DistinctionTheme.easy)
            } else {
                VStack(spacing: 0) {
                    Text("\(studyViewModel.reviewedWordCount)")
                        .font(.system(size: 22, weight: .bold, design: .rounded))
                    Text("/\(studyViewModel.dailyWordGoal)")
                        .font(.system(size: 11, weight: .medium))
                        .foregroundStyle(.secondary)
                }
            }
        }
    }

    private func startStudy(with book: VocabularyBook) {
        studyViewModel.selectedBook = book
        studyViewModel.resetSession()
        navigationPath.append(TodayDestination.study)
    }

    private var studyProgress: CGFloat {
        guard studyViewModel.dailyWordGoal > 0 else { return 0 }
        return min(1, CGFloat(studyViewModel.reviewedWordCount) / CGFloat(studyViewModel.dailyWordGoal))
    }
}

private enum TodayDestination: Hashable {
    case study
}

private struct TodayBookRow: View {
    let book: VocabularyBook
    let onTap: () -> Void

    var body: some View {
        Button(action: onTap) {
            HStack(spacing: 16) {
                BookCoverView(book: book, size: .medium)

                VStack(alignment: .leading, spacing: 4) {
                    Text(book.title)
                        .font(DistinctionTheme.bookTitleFont)
                        .foregroundStyle(.primary)

                    Text("\(book.wordCount) 語")
                        .font(.subheadline)
                        .foregroundStyle(.secondary)
                }

                Spacer()

                Image(systemName: "chevron.right")
                    .font(.caption.weight(.semibold))
                    .foregroundStyle(.tertiary)
            }
            .padding(.horizontal, 16)
            .padding(.vertical, 14)
            .contentShape(Rectangle())
        }
        .buttonStyle(.plain)
    }
}

private struct StudySettingsSheet: View {
    @Bindable var studyViewModel: StudyViewModel
    let availableBooks: [VocabularyBook]
    @Environment(\.dismiss) private var dismiss

    var body: some View {
        NavigationStack {
            Form {
                Section("ブック") {
                    Picker("学習ブック", selection: $studyViewModel.selectedBook) {
                        Text("選択してください").tag(Optional<VocabularyBook>.none)
                        ForEach(availableBooks) { book in
                            Text(book.title).tag(Optional(book))
                        }
                    }
                }

                Section("今日の学習数") {
                    Stepper("\(studyViewModel.dailyWordGoal) 語", value: $studyViewModel.dailyWordGoal, in: 5...50, step: 5)
                }

                Section {
                    Text("忘却曲線に基づく学習プランを設定できます。")
                        .font(.footnote)
                        .foregroundStyle(.secondary)
                }
            }
            .navigationTitle("設定")
            .navigationBarTitleDisplayMode(.inline)
            .toolbar {
                ToolbarItem(placement: .confirmationAction) {
                    Button("完了") { dismiss() }
                }
            }
        }
        .presentationDetents([.medium])
    }
}
