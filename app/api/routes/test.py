
@app.get("/historique")
def get_historique(db : session = Depends(get_db), user_id : int = Depends(get_current_user_id)):
    
    stmt = select(Query).where(Query.uder_id == user_id)
    
    rslt = db.execute(stmt)
    
    



user = User(
    username= "zakaria",
    password= "password"
)

db.add(user)





const [usetoken,setusetoken] = usestate(False)


