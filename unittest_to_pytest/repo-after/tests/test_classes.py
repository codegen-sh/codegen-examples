# tests/test_classes.py

import pytest
import unittest
from unittest.mock import Mock, patch
from jj_classes.castle import Castle
from jj_classes.character import Character


class TestCastle():
    """Tests for the Castle class."""
    @pytest.fixture
    def setup_testcastle():
        castle = Castle("Test Castle")
    


    def test_castle_name(setup_testcastle, Castle):
        """Test that the castle name is set correctly."""
        assertEqual(castle.name, "Test Castle")

    def test_castle_boss(setup_testcastle, Castle):
        """Test that the default boss is Bowser."""
        assertEqual(castle.boss, "Bowser")

    def test_castle_world(setup_testcastle, Castle):
        """Test that the default world is Grass Land."""
        assertEqual(castle.world, "Grass Land")

    def test_has_access_granted(setup_testcastle, Castle):
        """Test that access is granted for the correct powerup."""
        character = Mock(powerup="Super Mushroom")
        assertTrue(castle.has_access(character))

    def test_has_access_denied(setup_testcastle, Castle):
        """Test that access is denied for an incorrect powerup."""
        character = Mock(powerup="Starman")
        assertFalse(castle.has_access(character))

    def test_empty_name_raises_error(setup_testcastle, Castle):
        """Test that an empty castle name raises a ValueError."""
        with assertRaises(ValueError):
            Castle("")


class TestCharacter():
    """Tests for the Character class."""
    @pytest.fixture
    def setup_testcharacter():
        character = Character("Mario")
    


    def test_character_name(setup_testcharacter, Character):
        """Test that the character name is set correctly."""
        assertEqual(character.name, "Mario")

    def test_default_powerup(setup_testcharacter, Character):
        """Test that the default powerup is None."""
        assertIsNone(character.powerup)

    def test_set_powerup(setup_testcharacter, Character):
        """Test setting a powerup."""
        character.powerup = "Fire Flower"
        assertEqual(character.powerup, "Fire Flower")

    def test_empty_name_raises_error(setup_testcharacter, Character):
        """Test that an empty character name raises a ValueError."""
        with assertRaises(ValueError):
            Character("")


class TestCastleAndCharacter(unittest.TestCase):
    """Tests for the interaction between Castle and Character."""
    @pytest.fixture
    def setup_testcastleandcharacter():
        character = Character("Mario")
    


    def test_character_has_access(setup_testcastleandcharacter, Character):
        """Test that a character with the correct powerup has access."""
        character.powerup = "Super Mushroom"
        assertTrue(castle.has_access(character))

    def test_character_denied_access(setup_testcastleandcharacter, Character):
        """Test that a character with the wrong powerup is denied access."""
        character.powerup = "Starman"
        assertFalse(castle.has_access(character))


if __name__ == "__main__":
    unittest.main()
