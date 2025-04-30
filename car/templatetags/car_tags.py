from django import template

register = template.Library()

@register.filter
def filter_rating(reviews, rating):
    """Filter reviews by rating value"""
    return [review for review in reviews if review.rating == int(rating)] 