import pytest
from main import BooksCollector

class TestBooksCollector:

    @pytest.fixture
    def collector(self):
     
        return BooksCollector()

    def test_add_new_book_add_one_book(self, collector):
  
        collector.add_new_book('Гордость и предубеждение')
        assert 'Гордость и предубеждение' in collector.get_books_genre()

    @pytest.mark.parametrize('name', [
        'A',                                         # Граничное значение: 1 символ
        '1234567890123456789012345678901234567890', # Граничное значение: 40 символов
    ])
    def test_add_new_book_valid_length_success(self, collector, name):
  
        collector.add_new_book(name)
        assert name in collector.get_books_genre()

    @pytest.mark.parametrize('name', [
        '',                                           # Невалидное значение: 0 символов
        'Эта строка содержит ровно сорок один символ!', # Невалидное значение: 41 символ
    ])
    def test_add_new_book_invalid_length_not_added(self, collector, name):
  
        collector.add_new_book(name)
        assert name not in collector.get_books_genre()

    def test_add_new_book_double_adding_not_duplicate(self, collector):

        collector.add_new_book('Дракула')
        collector.add_new_book('Дракула')
        assert len(collector.get_books_genre()) == 1

    def test_add_new_book_has_no_genre_by_default(self, collector):
    
        collector.add_new_book('Оно')
        assert collector.get_book_genre('Оно') == ''

    def test_set_book_genre_existing_book_and_valid_genre(self, collector):
      
        collector.add_new_book('Оно')
        collector.set_book_genre('Оно', 'Ужасы')
        assert collector.get_book_genre('Оно') == 'Ужасы'

    def test_set_book_genre_not_in_available_genres(self, collector):
    
        collector.add_new_book('Дюна')
        collector.set_book_genre('Дюна', 'Киберпанк')
        assert collector.get_book_genre('Дюна') == ''

    def test_get_books_with_specific_genre_success(self, collector):
   
        collector.add_new_book('Шерлок Холмс')
        collector.set_book_genre('Шерлок Холмс', 'Детективы')
        collector.add_new_book('Оно')
        collector.set_book_genre('Оно', 'Ужасы')
        
        detectives = collector.get_books_with_specific_genre('Детективы')
        assert 'Шерлок Холмс' in detectives
        assert 'Оно' not in detectives

    def test_get_books_for_children_excludes_age_rating(self, collector):

        collector.add_new_book('Король Лев')
        collector.set_book_genre('Король Лев', 'Мультфильмы')
        collector.add_new_book('Оно')
        collector.set_book_genre('Оно', 'Ужасы')

        children_books = collector.get_books_for_children()
        assert 'Король Лев' in children_books
        assert 'Оно' not in children_books

    def test_add_book_in_favorites_success(self, collector):

        collector.add_new_book('Маска')
        collector.add_book_in_favorites('Маска')
        assert 'Маска' in collector.get_list_of_favorites_books()

    def test_add_book_in_favorites_not_in_collector_not_added(self, collector):
        collector.add_book_in_favorites('Несуществующая книга')
        assert 'Несуществующая книга' not in collector.get_list_of_favorites_books()

    def test_delete_book_from_favorites_success(self, collector):
        collector.add_new_book('Маска')
        collector.add_book_in_favorites('Маска')
        collector.delete_book_from_favorites('Маска')
        assert 'Маска' not in collector.get_list_of_favorites_books()