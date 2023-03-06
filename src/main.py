from repository.board_repository import BoardRepository
from services.board_services import BoardService
from services.board_validator import BoardValidator
from ui.ui import UI

if __name__== '__main__':
    repo = BoardRepository()
    valid = BoardValidator()
    serv = BoardService(valid, repo)
    run = UI(serv)
    run.start()
