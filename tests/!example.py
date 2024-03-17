import marsFile as mars
import titaniaLib as titania
from titaniaLib import Oberon as oberon

# print(mars.lookUp(".\\!example.mfc", "marsFile", "example", False))
mars.override(".\\!example.mfc","marsFile","users",['mercury','jupiter','saturn'])
print(mars.lookUp(".\\!example.mfc","marsFile","users"))
