from app.models.base_model import BaseModel

class Review(BaseModel):
    def init(self, text, rating, place, user):
        super().init()
        if not text:
            raise ValueError("Review text is required")
        if not (1 <= rating <= 5):
            raise ValueError("Rating must be between 1 and 5")

        self.text = text
        self.rating = rating
        self.place = place
        self.user  =  user
