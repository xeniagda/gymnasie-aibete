using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class GameState
{
    enum Action {Left, Right, Forward, Back, Shoot};
    


    public GameState() {

    }

    // Update is called once per frame
    void Update(Action action)
    {
        switch(action) {
            case Action.Left:
                break;
            case Action.Right:
                break;
            case Action.Forward:
                break;
            case Action.Back:
                break;
            case Action.Shoot:
                break;
        }    
    }


}
