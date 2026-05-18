from __future__ import annotations
from dataclasses import dataclass, field
from typing import Any


@dataclass
class UserState:
    
    state: str = "idle"
    context: dict[str, Any] = field(default_factory=dict)
    
class conversationState:
        
    def __init__(self) -> None:
        self._store: dict[str, UserState] = {}
            
        #lectura 
    def get_state(self, numero: str) -> str:
        return self._store.get(numero, UserState()).state
        
    def get_context(self, numero: str) -> dict[str, Any]:
        return self._store.get(numero, UserState()).context
        
    def get_full(self, numero: str) -> UserState:
        if numero not in self._store:
            self._store[numero] = UserState()
        return self._store[numero]
        
        #Escritura
    def set_state(self, numero: str, state: str, context: dict | None = None) ->None:
        user = self.get_full(numero)
        user.state = state
        if context: 
            user.context.update(context)
                
    def reset(self, numero: str) -> None:
        self._store[numero] = UserState(state="idle")
        
        #Utilidades
    def snapshot(self) -> dict:
        return {k: {"state": v.state, "context": v.context}
                for k, v in self._store.items()}

#singleton global para manejar estados de conversación (en memoria, por simplicidad)        
conversation_state = conversationState()