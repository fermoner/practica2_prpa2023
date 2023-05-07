# prpa-practica2

Se simula el problema del puente de Ambite y se implementan algoritmos para su resolución.
Puesto que las distintas clases de usuarios del puente se comportan de forma simétrica, se hace usos de la clase Enum de python que permite implementar funciones generales que sirven para las 3 clases.

## Practica2_V1
Resuelve el problema mediante una variable condición para cada clase, que bloquea a los usuarios de dicha clase mientras haya usuarios de otra clase cruzando el puente. Las clases se van cediendo el paso de forma cíclica. Este algoritmo sufre inanición de los vehículos por un flujo constante de peatones, ya que los peatones tardan en cruzar más de lo que tardan en llegar nuevos peatones.

## Practica2_V2
Es una ligera modificación del algoritmo anterior que resuelve inanición haciendo que los usuario de una determianda clase no puedan comenzar a cruzar, si cuando llegarón al puente ya había miembros de su misma clase cruzando.

## Practica2_PuenteDeAmbite
Explicación más extensa de los algortimos implementados y su corrección usando la abstracción del libro de Ben-Ari "Principles of concurrent and distributed programming".
