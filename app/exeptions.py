"""
Кастомні виключення:
- ConversionError: базова помилка конвертації
- UnsupportedFormatError: формат не підтримується
- EmptyArchiveError: архів порожній або не містить підтримуваних файлів
"""


class ConversionError(Exception):
    """Загальна помилка конвертації файлу."""


class UnsupportedFormatError(ConversionError):
    """Формат вхідного файлу не підтримується."""


class EmptyArchiveError(ConversionError):
    """Архів не містить підтримуваних файлів або є порожнім."""
