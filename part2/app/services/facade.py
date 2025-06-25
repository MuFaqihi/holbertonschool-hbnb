from app.persistence.repository import InMemoryRepository
from app.models.user import User
from app.models.place import Place
from app.models.review import Review
from app.models.amenity import Amenity


class HBnBFacade:
    def __init__(self):
        self.user_repo = InMemoryRepository()
        self.place_repo = InMemoryRepository()
        self.review_repo = InMemoryRepository()
        self.amenity_repo = InMemoryRepository()

    def create_user(self, user_data):
        user = User(**user_data)
        self.user_repo.add(user)
        return user

    def get_user(self, user_id):
        return self.user_repo.get(user_id)

    def get_user_by_email(self, email):
        return self.user_repo.get_by_attribute('email', email)

    def get_all_users(self):
        return self.user_repo.get_all()

    def update_user(self, user_id, user_data):
        user = self.user_repo.get(user_id)
        if not user:
            return None

        user.validate()
        if 'first_name' in user_data:
            user.first_name = user_data['first_name']
        else:
            raise TypeError('first_name must be in payload') 
        
        if 'last_name' in user_data:
            user.last_name = user_data['last_name']
        else:
            raise TypeError('last_name must be in payload')
        
        if 'email' in user_data:
            user.email = user_data['email']
        else:
            raise TypeError('email must be in payload')

        for key, value in user_data.items():
            if hasattr(user, key):
                setattr(user, key, value)

        self.user_repo.update(user_id, user)
        return user

    def create_place(self, place_data):
        owner = self.user_repo.get(place_data['owner_id'])
        if not owner:
            raise ValueError("Invalid owner_id")

        for amenity_id in place_data.get("amenities", []):
            if not self.amenity_repo.get(amenity_id):
                raise ValueError(f"Amenity {amenity_id} does not exist")

        place = Place(**place_data)
        self.place_repo.add(place)
        return place

    def get_place(self, place_id):
        place = self.place_repo.get(place_id)
        if not place:
            return None

        owner = self.user_repo.get(place.owner_id)
        amenities = [self.amenity_repo.get(aid) for aid in place.amenities]

        return {
            "id": place.id,
            "title": place.title,
            "description": place.description,
            "price": place.price,
            "latitude": place.latitude,
            "longitude": place.longitude,
            "owner": {
                "id": owner.id,
                "first_name": owner.first_name,
                "last_name": owner.last_name,
                "email": owner.email
            } if owner else None,
            "amenities": [
                {"id": a.id, "name": a.name} for a in amenities if a is not None
            ]
        }

    def get_all_places(self):
        return [
            {
                "id": p.id,
                "title": p.title,
                "latitude": p.latitude,
                "longitude": p.longitude
            } for p in self.place_repo.get_all()
        ]

    def update_place(self, place_id, place_data):
        place = self.place_repo.get(place_id)
        if not place:
            return None

        if "price" in place_data and place_data["price"] < 0:
            raise ValueError("Price must be non-negative")

        if "latitude" in place_data and not (-90 <= place_data["latitude"] <= 90):
            raise ValueError("Latitude must be between -90 and 90")

        if "longitude" in place_data and not (-180 <= place_data["longitude"] <= 180):
            raise ValueError("Longitude must be between -180 and 180")

        if "amenities" in place_data:
            for aid in place_data["amenities"]:
                if not self.amenity_repo.get(aid):
                    raise ValueError(f"Amenity {aid} does not exist")

        for key, value in place_data.items():
            if hasattr(place, key):
                setattr(place, key, value)

        self.place_repo.update(place_id, place)
        return place

    def create_amenity(self, amenity_data):
        amenity = Amenity(**amenity_data)
        self.amenity_repo.add(amenity)
        return amenity

    def get_amenity(self, amenity_id):
        return self.amenity_repo.get(amenity_id)

    def get_all_amenities(self):
        return self.amenity_repo.get_all()

    def update_amenity(self, amenity_id, amenity_data):
        amenity = self.amenity_repo.get(amenity_id)
        if amenity:
            for key, value in amenity_data.items():
                if hasattr(amenity, key):
                    setattr(amenity, key, value)
            self.amenity_repo.update(amenity_id, amenity)
        return amenity

    def create_review(self, review_data):
        review = Review(**review_data)
        self.review_repo.add(review)
        return review

    def get_review(self, review_id):
        return self.review_repo.get(review_id)

    def get_all_reviews(self):
        return self.review_repo.get_all()

    def get_reviews_by_place(self, place_id):
        return [
            review for review in self.review_repo.get_all()
            if review.place_id == place_id
        ]

    def update_review(self, review_id, review_data):
        review = self.review_repo.get(review_id)
        if not review:
            return None
        for key, value in review_data.items():
            if hasattr(review, key):
                setattr(review, key, value)
        self.review_repo.update(review_id, review)
        return review

