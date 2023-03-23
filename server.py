from flask import Flask, render_template, request, redirect, url_for, jsonify
import random
app = Flask(__name__) 

# THIS CODE ROUTES THE USER TO THE HOME PAGE
@app.route('/', methods=["POST", "GET"]) 
def home():
    # IF A POST REQUEST IS SENT
    if request.method == "POST":
        # STORE THE USER NAMES AND REDIRECT TO DICE GAME PAGE
        p1_name = request.form.get("p1")
        p2_name = request.form.get("p2")
        return redirect(url_for('game', p1_name=p1_name, p2_name=p2_name))
    else:
        return render_template("home.html")

# ROUTES USER TO THE DICE GAME PAGE
@app.route('/game', methods=["POST", "GET"])
def game():
        # USING THE REQUEST OBJECT FETCH THE PLAYER NAMES
        player1 = request.args.get('p1_name')
        player2 = request.args.get('p2_name')
        # RENDER THE GAME HTML TEMPLATE
        return render_template("game.html", p1_name=player1, p2_name=player2)

# AJAX SENDS REQUESTS TO THIS URL
# AJAX ALLOWS THE CLIENT AND SERVER TO COMMUNICATE
@app.route('/process')
def process():
    # CHECK IF BUTTON CLICKED IS ROLL OR HOLD
    text = request.args.get('button_text')
    text2 = request.args.get('dice_img')
    p1_name = request.args.get('p1_name')
    p2_name = request.args.get('p2_name')
    text4 = request.args.get('score1')
    text5 = request.args.get('score2')

    # DEFAULT PLAYER SCORES = 0
    score1 = 0
    score2 = 0

    # AJAX SENDS A JSON REQUEST
    if request.is_json:
        # RETURNS AN JSON OBJECT KEY/VALUE PAIR
        # YOU CAN ADD WHATEVER YOU WANT 
        # KEY MUST MATCH THE AJAX        
       
        # CHANGING THE DICE NUMBER 
        dice_number = random.randint(1, 6)
        dice_filename = 'dice' + str(dice_number) + ".png"
        dice_file_path = "/static//"
        dice = dice_file_path + dice_filename

        # CHECK WHO'S TURN IT IS
        if request.args.get('player_turn') == p1_name:
            
            # DEBUGGING
            print()
            print('Button Clicked: ', text)
            print('Dice Number: ', dice_number)
            print('Player 1 Name: ', p1_name)
            print('Current Player Turn: ', request.args.get('player_turn'))
            print('Player 2 Name: ', p2_name)
            print('Player 1 Score: ', text4)
            print('Player 2 Score: ', text5)
            print()

            # CHECK WHICH BUTTON WAS CLICKED

            # ------------------------
            # CHOICE 1:  ROLL THE DICE
            # ------------------------
            if request.args.get('button_text') == 'ROLL':
            # CHANGING PLAYER SCORE

                if dice_number == 1:
                    return jsonify({'dice': dice, 'score1': 0, 'score2': 0, 'turn' : request.args.get('p2_name'), 'dice_num': dice_number })



                score1 = str(dice_number)

            # RESPONSE SENT BACK TO THE CLIENT IN THE FORM OF JSON
                return jsonify({'dice': dice, 'score1': score1, 'score2': 0,'turn' : request.args.get('p1_name')})

            # ------------------------
            # CHOICE 2:  HOLD THE DICE
            # ------------------------

            elif request.args.get('button_text') == 'HOLD': 
                print("--- PLAYER 2 TURN ---")
                return jsonify({'dice': dice, 'score1': 0, 'turn' : request.args.get('p2_name')})

        # ------------------------
        # PLAYER 2 TURN
        # ------------------------
        elif request.args.get('player_turn') == p2_name:
            print()
            print('Button Clicked: ', text)
            print('Dice Number: ', dice_number)
            print('Player 1 Name: ', p1_name)
            print('Current Player Turn: ', request.args.get('player_turn'))
            print('Player 2 Name: ', p2_name)
            print('Player 1 Score: ', text4)
            print('Player 2 Score: ', text5)
            print()

            # ------------------------
            # CHOICE 1:  ROLL THE DICE
            # ------------------------
            if request.args.get('button_text') == 'ROLL':
                
                if dice_number == 1:
                    return jsonify({'dice': dice, 'score1': 0, 'score2': 0, 'turn' : request.args.get('p1_name'), 'dice_num': dice_number })
                
                    
                score2 = str(dice_number)

                return jsonify({'dice': dice, 'score1': 0,  'score2': score2, 'turn' : request.args.get('p2_name')})
            
            # ------------------------
            # CHOICE 2:  HOLD THE DICE
            # ------------------------
            
            elif request.args.get('button_text') == 'HOLD': 
                print("--- PLAYER 1 TURN ---")
                return jsonify({'dice': dice, 'turn' : request.args.get('p1_name')})

        # RESPONSE SENT BACK TO THE CLIENT
        return jsonify({'dice': dice, 'score1': score1, 'score2': score2, 'turn' : request.args.get('p1_name'), 'dice_num': dice_number })
    else : 
        return "404 Error"



if __name__ == '__main__': 
    app.run()