# Programming conventions #
  * Pythonic as possible (this is a learning project)
```
class Example :
      def __init__(self) :
      	  self.variable = 0
      	  pass
      def methodOfExample(self) :
      	  pass 
```

  * Each major class has a test method which can also be used as an example, so using class Example, has a method which also returns an instance of the class
```
def ExampleTest() :
    et = Example()
    return et
```