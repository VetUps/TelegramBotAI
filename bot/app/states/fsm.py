from aiogram.fsm.state import State, StatesGroup

class BotStates(StatesGroup):
                                   
                                                                                    
    waiting_for_game_name = State()
    
                                 
                                                           
    ai_chat_mode = State()                                 
    ai_image_mode = State()                              
    ai_video_mode = State()                               
    
                                              
                                                              
    waiting_for_sentiment_text = State()