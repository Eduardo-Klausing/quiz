import pytest
from model import Question

def test_create_question():
    question = Question(title='q1')
    assert question.id != None

def test_create_multiple_questions():
    question1 = Question(title='q1')
    question2 = Question(title='q2')
    assert question1.id != question2.id

def test_create_question_with_invalid_title():
    with pytest.raises(Exception):
        Question(title='')
    with pytest.raises(Exception):
        Question(title='a'*201)
    with pytest.raises(Exception):
        Question(title='a'*500)

def test_create_question_with_valid_points():
    question = Question(title='q1', points=1)
    assert question.points == 1
    question = Question(title='q1', points=100)
    assert question.points == 100

def test_create_choice():
    question = Question(title='q1')
    
    question.add_choice('a', False)

    choice = question.choices[0]
    assert len(question.choices) == 1
    assert choice.text == 'a'
    assert not choice.is_correct


def test_create_question_with_invalid_points_below_range():
    with pytest.raises(Exception):
        Question(title='q1', points=0)


def test_create_question_with_invalid_points_above_range():
    with pytest.raises(Exception):
        Question(title='q1', points=101)


def test_add_multiple_choices_and_ids_increment():
    q = Question(title='q1')
    c1 = q.add_choice('a')
    c2 = q.add_choice('b')
    assert c1.id == 1
    assert c2.id == 2


def test_remove_choice_by_id_removes_correct_choice():
    q = Question(title='q1')
    c1 = q.add_choice('a')
    c2 = q.add_choice('b')
    q.remove_choice_by_id(c1.id)
    assert [c.id for c in q.choices] == [c2.id]


def test_remove_choice_by_id_invalid_raises_exception():
    q = Question(title='q1')
    q.add_choice('a')
    with pytest.raises(Exception):
        q.remove_choice_by_id(999)


def test_remove_all_choices_clears_list():
    q = Question(title='q1')
    q.add_choice('a')
    q.add_choice('b')
    q.remove_all_choices()
    assert q.choices == []


def test_set_correct_choices_marks_choice_correct():
    q = Question(title='q1')
    c1 = q.add_choice('a')
    c2 = q.add_choice('b')
    q.set_correct_choices([c2.id])
    assert not c1.is_correct
    assert c2.is_correct


def test_set_correct_choices_with_invalid_id_raises():
    q = Question(title='q1')
    q.add_choice('a')
    with pytest.raises(Exception):
        q.set_correct_choices([999])


def test_correct_selected_choices_returns_only_correct():
    q = Question(title='q1')
    c1 = q.add_choice('a', is_correct=True)
    c2 = q.add_choice('b', is_correct=False)

    selected = q.correct_selected_choices([c1.id])
    assert selected == [c1.id]


def test_correct_selected_choices_exceeds_max_selections_raises():
    q = Question(title='q1', max_selections=1)
    c1 = q.add_choice('a', is_correct=True)
    c2 = q.add_choice('b', is_correct=True)
    with pytest.raises(Exception):
        q.correct_selected_choices([c1.id, c2.id])

# ----------------- FIXTURES -----------------

@pytest.fixture
def sample_question():
    """Retorna uma questão com 3 escolhas, 2 corretas."""
    q = Question(title="Sample question", max_selections=3)  
    c1 = q.add_choice("Choice A", is_correct=True)
    c2 = q.add_choice("Choice B", is_correct=False)
    c3 = q.add_choice("Choice C", is_correct=True)
    return q

@pytest.fixture
def empty_question():
    """Retorna uma questão sem escolhas."""
    return Question(title="Empty question")

# ----------------- TESTS USANDO FIXTURES -----------------

def test_correct_choices_with_fixture(sample_question):
    """Verifica se apenas as escolhas corretas são retornadas."""
    correct_ids = sample_question.correct_selected_choices(
        [c.id for c in sample_question.choices]
    )
    # Deve retornar apenas os IDs das escolhas corretas (Choice A e C)
    expected_ids = [c.id for c in sample_question.choices if c.is_correct]
    assert correct_ids == expected_ids

def test_add_and_remove_choices_with_fixture(empty_question):
    """Testa adicionar e remover escolhas usando fixture."""
    # Adiciona escolhas
    c1 = empty_question.add_choice("A")
    c2 = empty_question.add_choice("B")
    assert len(empty_question.choices) == 2

    # Remove a primeira escolha
    empty_question.remove_choice_by_id(c1.id)
    assert len(empty_question.choices) == 1
    assert empty_question.choices[0].id == c2.id