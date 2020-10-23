from Engine import ConversationalEngine
from ArticulationMapper import ArticulationMapper
from collections import namedtuple
class Conversation():
    def __init__(self, app, engine: ConversationalEngine, trainingdata: str, articulationdata: str):
        super().__init__()
        self.app=app
        self.engine = engine
        self.utterances = []
        self.responses = []
        self.interactions = []
        self.articMapper = ArticulationMapper(articulationdata)
    
    def interact(self, utterance: str, returnPayload = False):
        self.utterances.append(utterance)
        response = self.engine.getIntent(utterance)
        self.responses.append(response.get('intent'))
        if response.get('probability') > 0.3:
            articulation = self.articMapper.get(response.get('intent'))
            if articulation == None:
                articulation = self.articMapper.get('no_articulation')
        else:
            articulation = self.articMapper.get('mishandled')
        Interaction = namedtuple('Interaction', ['utterance', 'response'])
        self.interactions.append(Interaction(utterance, articulation))
        if returnPayload == False:
            return articulation
        else:
            return {
                'articulation' : articulation,
                'intent' : response.get('intent'),
                'probability' : response.get('probability'),
                'probability_matrix' : response.get('probability_matrix')
            }

    def get(self):
        '''returns all the interactions for the conversation as a list'''
        return self.interactions
    
    def getConvoLength(self):
        '''returns the conversation length'''
        return len(self.interactions)
    
def main():
    engine = ConversationalEngine(app=None)
    convo = Conversation(app=None, engine=engine)
    while 1: 
        entry=input()
        print(convo.interact(entry))

if __name__=="__main__":
    main()