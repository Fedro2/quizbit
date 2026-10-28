# 🧠💡 Quizbit – Learning Set Project

Quizbit is the first project for the Programming Foundations course at FHNW, BSc BIT. It is a simple Python console application for creating, managing, and studying learning sets stored as Excel files.

## 📝 Analysis


### Problem 

Students need to practise questions and answers when preparing for exams. Reading notes alone makes it difficult to check whether they can recall an answer without looking it up. They also need to organise their learning material and revisit questions they have answered incorrectly.

---
### Scenario

A student prepares questions and answers in an Excel file or creates a learning set directly in Quizbit. The student selects a saved set and starts a learning session in the terminal. Quizbit displays one question at a time, checks the student's answer, and repeats incorrectly answered questions until every question has been answered correctly. The student can also edit the set, quit a session, or restart it.

## 👤 User Roles


| Role | Description |
| --- | --- |
| Learner | Studies saved learning sets, answers questions, and uses feedback to practise recall. |
| Set creator | Creates, imports, and maintains questions and answers in learning sets. |

One person can act as both a learner and a set creator.

## 📖 User Stories


### US-01: Import a learning set 


As a learner, I want to see my progress and a session summary, so that I can understand how much I have learned and which questions remain.

**Acceptance criteria**<br><br>
During a session, show the number of questions mastered and remaining out of the selected session size.
On completion or quitting, show correct attempts, incorrect attempts, total attempts, questions mastered, questions remaining, and accuracy.
Given two questions are answered correctly after one incorrect attempt, the summary shows 2 mastered, 0 remaining, 3 attempts, and 66.7% accuracy.
If no answers have been submitted, show 0 attempts and 0.0% accuracy. Blank answers and commands do not count as attempts.

---

### US-02: View and select learning sets Julia

**As** a learner, I want to see all saved learning sets and select one, so that I can study or edit my chosen topic.

**Acceptance criteria**<br><br>
- Display saved CSV sets as an alphabetically sorted, numbered list starting at 1.
- Selecting a listed number opens that set and displays its available actions.
- If there are no sets, display a message and return to the main menu. Invalid numbers or text display an error and
allow another selection.

---

### US-03: Create a new learning set

**As** a set creator, I want to create a named learning set, so that I can organise questions for a particular topic.


**Acceptance criteria**<br><br>
- Entering an available name opens an empty set that can be filled with questions.
- Reject empty names, names containing path separators, and names already used by another saved set; ask for a
different name.
- Creating a set does not change existing sets. The new set is kept in memory until explicitly saved.

---

### US-04: Add questions and answers

**As** a set creator, I want to add a question and its predefined short answer, so that I can extend a learning set
with material to practise.

**Acceptance criteria**<br><br>
- Entering a question and answer adds exactly one pair to the current set and displays confirmation.
- Reject empty or whitespace-only questions and answers without adding an incomplete pair.
- Remove surrounding spaces. Reject /quit and /restart as answers because they are reserved session commands.
---
### US-05: Edit questions and answers

**As** a set creator, I want to edit existing questions and answers, **so that** I can correct mistakes or improve the content.


**Acceptance criteria**<br><br>
- Display numbered question-answer pairs and allow the creator to select one for editing.
- Replacing the selected question and answer changes only that pair; after saving and reopening, the replacement is still present.
- Reject invalid selection numbers and empty replacement fields. Cancelling the selection leaves the set unchan

---

### US-06: Delete questions

**As** a set creator, I want to delete individual questions from a learning set, **so that** I can remove content I no longer need.


**Acceptance criteria**<br><br>
- Display the selected pair and request confirmation before deleting it.
- Confirming deletion in a three-pair set removes exactly the selected pair and leaves two pairs. Declining changes nothing.
- Invalid selections or confirmations allow another attempt. An empty set cannot be studied or saved over an existing set.

---

### US-07: Save a learning set as an Excel file

**As** a learner, I want to choose how many questions to practise in a session, **so that** I can adapt the session to the time I have available.


**Acceptance criteria**<br><br>
- For a set of N questions, accept a whole number from 1 to N; pressing Enter selects all N questions.
- Selecting 3 questions from a ten-question set includes exactly 3 question rows in the session. Repetitions of wrong answers do not increase that selection.
- Reject 0, negative numbers, numbers greater than N, decimals, and text, then request the number again.
- Session selection leaves the full saved set unchanged. An empty set cannot start a session.

---

### US-08: Start a learning session

**As** a learner, I want to start a learning session for a selected learning set, **so that** I can practise my knowledge.

**Acceptance criteria**<br><br>
- After the learner chooses session size and order, display the first selected question and request an answer.
- Display one question at a time without revealing its stored answer before submission.
- An empty set displays a message instead of starting a session. Studying does not change the saved questions or
answers.

---

### US-09: Receive feedback on my answer

**As** a learner, I want to know whether each answer is correct or incorrect, **so that** I can assess my knowledge.

**Acceptance criteria**<br><br>
- Compare the complete entered and stored answers after trimming surrounding spaces and ignoring capitalisation.
- Given the stored answer is def, an input of " DEF " is correct; function or de is incorrect. Show the stored answer
after an incorrect attempt.
- Do not assess unrestricted written responses, synonyms, or partial matches automatically.
- An empty input requests another answer for the same question. Session commands are handled separately from
answer checking.

---

### US-10: Repeat incorrectly answered questions

**As** a learner, I want incorrectly answered questions to appear again, **so that** I can practise until I have answered every question correctly.

**Acceptance criteria**<br><br>
- An incorrect answer moves its question to the end of the remaining questions. A correct answer removes its
question from the current session.
- Given question 1 is wrong and questions 2 and 3 are correct, question 1 appears again after question 3.
- If the last remaining question is wrong, it is asked again. Complete the session only when every selected question
has been answered correctly at least once.

---

### US-11: Quit a learning session

As a learner, I want to choose random question order, so that I practise recall without relying on a familiar sequence.

**Acceptance criteria**<br><br>
Before a session, offer file order and random order. Reject unsupported choices and request the choice again.
File order uses the first requested number of questions in their stored order. Random order shuffles the set and selects the requested number of question rows without selecting a row twice.
Randomising does not change the saved set. A one-question set still works; random order may match the original order by chance.

---

### US-12: Restart a learning session

As a learner, I want to restart an ongoing learning session, so that I can practise its selected questions again from the beginning.

**Acceptance criteria**<br><br>
Entering /restart at an answer prompt resets mastered questions and all attempt counters.
The same selected questions return to the session. File order is preserved, or the selected questions are shuffled again if random order was chosen.
Restarting before the first answer works. The command ignores capitalisation and surrounding spaces and does not change the saved set.

---

**Use cases:**

- Import a learning set from an Excel file
- View and select saved learning sets
- Create a learning set
- Add, edit, and delete question-answer pairs
- Save a learning set as an Excel file
- Start a learning session and receive feedback
- Repeat incorrectly answered questions until completion
- Quit or restart a learning session


## 👥 Team & Contributions


| Student | Responsible user stories | Contribution |
| --- | --- | --- |
| Julia | US-02, US-03, US-04 | Display and select sets, create named sets, add question-answer pairs |
| Lana | US-05, US-06, US-07 | Edit pairs, delete pairs, validate and choose session size |
| Pedro | US-08, US-09, US-10 | Start learning sessions, check short answers, repeat missed questions |
| Anis | US-01, US-11, US-12 | Show progress summaries, randomise question order, restart sessions |

## ✅ Project Requirements

### 1. Interactive App (Console Input)

Users interact through numbered terminal menus and text prompts. They can create and edit sets, select a set,
choose session size and order, answer questions, and view feedback and summaries. Commands allow
restarting or quitting a learning session.

### 2. Data Validation

The application checks menu and question numbers, rejects empty questions and answers, and requires the
session size to be a whole number within the selected set's size. Set names cannot be empty, contain path
separators, or duplicate another saved name. Invalid input displays an explanatory message and allows another
attempt. CSV loading rejects missing fields, invalid headers, unreadable files, and empty sets without starting a
session.
Answer checking compares only predefined short answers. It ignores capitalisation and surrounding spaces and
otherwise requires a full match; it does not evaluate unrestricted written responses.

### 3. File Processing

Learning sets are read from and written to CSV files using Python's built-in csv module. Creating or editing a set
and choosing Save writes its question-answer pairs to the saved-sets folder. Reopening the file loads the saved
content. Importing loads a separate CSV file without changing the original. Failed saves show an error and keep
the current edits available for another attempt.


## 🔄 Team Workflow


We organise our work around the user stories in this README. Each task is linked to a user story so that changes can be traced back to the feature they support.

---

### Branches and Commits

Before working on a user story, we create a separate branch from the latest version of `main`. Branch names include the user story number and a short description, for example `us-01-import-learning-set`.

Commit messages include the corresponding user story number and describe the change, for example `US-01: Add learning set import`. This keeps the project history clear and makes it easier to understand which changes belong to each story.

---

### Pull Requests and Reviews

When the work is ready for review, the author opens a pull request into `main`.

At least two other team members must review and approve the pull request before it can be merged. If further code changes are made after approval, reviewers review the updated version again.


## ⚙️ Implementation

...
