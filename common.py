class SubclassShouldImplement(Exception):
    def __init__(self, msg="A method was called which should have been overridden"):
        Exception.__init__(self,msg)
