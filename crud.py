from sqlalchemy.orm import Session
from sqlalchemy.orm import joinedload
from sqlalchemy import or_, and_
from models import Category, subCategory, Product, Users, Image
from upload_depends import upload_image, delete_uploaded_image


def create_crud(req, model, db: Session):
    new_add = model(**req.dict())
    db.add(new_add)
    db.commit()
    db.refresh(new_add)
    return new_add


def read_category(db: Session):
    result = db.query(Category).options(joinedload(Category.subcategory)).all()
    return result


def read_product(category_id, subcategory_id, db: Session):
    result = db.query(
        Product,

    ).options(joinedload(Product.image).load_only('img'))\
    .join(Category, Category.id == Product.category_id)\
    .join(subCategory, subCategory.id == Product.subcategory_id)
    
    if category_id:
        result = result.filter(Product.category_id == category_id)
    if subcategory_id:
        result = result.filter(Product.subcategory_id == subcategory_id)
    result = result.all()
    return result



def signIn(req, db: Session):
    user = db.query(Users.token).filter(
        and_(
            or_(
                Users.phone_number == req.phone_number,
                Users.username == req.username,
                Users.age_feature == req.age_feature,
                Users.skin_position == req.skin_position
            ),
        )
    ).first()
    if user:
        return user
    
    
def read_users(header_param, db: Session):
    username: str = payload.get('username')
    user = db.query(Users)\
        .filter(
            and_(
                Users.username == username, 
                Users.phone_number == phone_number, 
                Users.age_feature == age_feature,
                Users.skin_position == skin_position
            )
        )\
            .first()
    if user:
        return db.query(Users).all()
    else:
        return False



def create_img(id, file, db: Session):
    uploaded_file_name = upload_image('product', file)
    new_add = Image(
        img = uploaded_file_name,
        product_id = id
    )
    db.add(new_add)
    db.commit()
    db.refresh(new_add)
    return new_add


def delete_img(id, db: Session):
    image = db.query(Image).filter(Image.id == id).first()
    if image.img:
        delete_uploaded_image(image_name=image.img)
        db.query(Image).filter(Image.id == id)\
            .delete(synchronize_session=False)
        db.commit()
    return True