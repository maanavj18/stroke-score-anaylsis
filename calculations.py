import numpy as np

#Gets angle between joints
def joint_angle(pt1, pivot, pt2):
    v1 = pt1 - pivot
    v2 = pt2 - pivot
    angleNA = np.arccos(np.clip(np.dot(v1, v2) / (np.linalg.norm(v1) * np.linalg.norm(v2)), -1.0, 1.0))
    return np.degrees(angleNA)


def distance(pt1, pt2):
    v1 = np.array([pt2.x - pt1.x, pt2.y - pt1.y, pt2.z - pt1.z])
    return np.linalg.norm(v1)

def velocity(frames, landmark_index):
    if len(frames) < 2:
        return 0.0

    avg_speed = 0.0
    count = 0
    for i in range(len(frames) - 1):
        timeDiff = frames[i+1].timestamp - frames[i].timestamp

        if frames[i].pose_world_landmarks is None or frames[i+1].pose_world_landmarks is None:
            continue

        dist = distance(frames[i].pose_world_landmarks[landmark_index], frames[i+1].pose_world_landmarks[landmark_index])
        speed = float(dist)/float(timeDiff)
        avg_speed += speed
        count+=1

    if count > 0:
        avg_speed/= count
    else:
        avg_speed = 0.0

    return avg_speed

def position(landmark, index):
    pt = landmark[index]
    position = np.array([pt.x, pt.y, pt.z])
    return position

def avg_position(frames, landmark_index):
    if not frames:
        return None
    
    avg_pos = np.zeros(3)
    count = 0
    for f in frames:
        if f.pose_world_landmarks is not None:
            avg_pos += position(f.pose_world_landmarks, landmark_index)
            count += 1

    if count == 0:
        return None
    return avg_position/(float(count))


def vertical_diff(pt1, pt2):
    return abs(pt1[1] - pt2[1])


