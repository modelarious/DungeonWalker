from exceptions import CameraGivenBadBounds

class Camera(object):
    def __init__(self, cameraWidth, cameraHeight):
        self.cameraWidth = cameraWidth # number of tiles wide that should be displayed
        self.cameraHeight = cameraHeight # number of tiles tall that should be displayed
    
    def watch_character(self, characterModel):
        self.playerModel = characterModel
    
    def watch_map(self, mapModel):
        self.mapModel = mapModel
    
    def get_camera_box(self):
        playerX, playerY = self.playerModel.get_pos()
        mapWidth, mapHeight = self.mapModel.get_width(), self.mapModel.get_height()
        halfCameraWidth = (self.cameraWidth // 2)
        halfCameraHeight = (self.cameraHeight // 2)

        if self.cameraWidth > mapWidth or self.cameraHeight > mapHeight:
            raise CameraGivenBadBounds(f"cameraWidth {self.cameraWidth} exceeds mapWidth {mapWidth} or cameraHeight {self.cameraHeight} exceeds mapHeight {mapHeight}")

        minX = max(0, playerX - halfCameraWidth) # ensure we don't go out of bounds on the left
        minY = max(0, playerY - halfCameraHeight) # ensure we don't go out of bounds on the top
        maxX = minX + self.cameraWidth
        maxY = minY + self.cameraHeight

        # minX and minY are great unless we are at the bottom or right-hand side of the screen.
        # we need to make sure that we aren't exceeding the bounds of the map.
        # we do this by shifting the camera over if we are out of bounds on either the right or bottom.
        if mapWidth < maxX:
            delta = maxX - mapWidth
            minX -= delta
            maxX -= delta
        if mapHeight < maxY:
            delta = maxY - mapHeight
            minY -= delta
            maxY -= delta
        
        cameraBox = (minX, maxX, minY, maxY)
        
        # now we ensure that we aren't returning any negative values
        if any([val < 0 for val in cameraBox]):
            raise CameraGivenBadBounds(f"a value in the camera box was less than 0: {cameraBox}")

        return cameraBox
    
    def get_player_draw_position(self):
        # if this is the character that we are tracking with the camera
        # if characterModel == self.playerModel:
        playerX, playerY = self.playerModel.get_pos()
        (minX, _, minY, _) = self.get_camera_box()
        return playerX - minX, playerY - minY
        
        # if this is one of the characters we aren't tracking with the camera


        

