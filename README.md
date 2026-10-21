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


**As** a set creator, I want to import an Excel file containing questions and answers, **so that** I can use an existing learning set.

**Acceptance criteria**<br><br>
*To be defined...*

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
*To be defined...*

---

### US-06: Delete questions

**As** a set creator, I want to delete individual questions from a learning set, **so that** I can remove content I no longer need.


**Acceptance criteria**<br><br>
*To be defined...*

---

### US-07: Save a learning set as an Excel file

**As** a set creator, I want to save new or edited learning sets as Excel files, **so that** my changes are preserved and I can use the sets again later.


**Acceptance criteria**<br><br>
*To be defined...*

---

### US-08: Start a learning session

**As** a learner, I want to start a learning session for a selected learning set, **so that** I can practise my knowledge.

**Acceptance criteria**<br><br>
*To be defined...*

---

### US-09: Receive feedback on my answer

**As** a learner, I want to know whether each answer is correct or incorrect, **so that** I can assess my knowledge.

**Acceptance criteria**<br><br>
*To be defined...*

---

### US-10: Repeat incorrectly answered questions

**As** a learner, I want incorrectly answered questions to appear again, **so that** I can practise until I have answered every question correctly.

**Acceptance criteria**<br><br>
*To be defined...*

---

### US-11: Quit a learning session

**As** a learner, I want to quit an ongoing learning session at any time, **so that** I can return to the main menu.

**Acceptance criteria**<br><br>
*To be defined...*

---

### US-12: Restart a learning session

**As** a learner, I want to restart an ongoing learning session, **so that** I can practise the entire learning set again from the beginning.

**Acceptance criteria**<br><br>
*To be defined...*

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


| Name             | Contribution |
|------------------| --- |
| Ferrari Pedro    | To be decided |
| Tabakovic Anis   | To be decided |
| Cabalzar Julia   | US-02, US-03, US-04 |
| Redjepi Ulpijana | To be decided |

## ✅ Project Requirements


To be accepted, the project must meet the following requirements:

1. Interactive app (console input)
2. Data validation (input checking)
3. File processing (read/write)

---

### 1. Interactive App (Console Input)

...

---

### 2. Data Validation

...

---

### 3. File Processing

...


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
