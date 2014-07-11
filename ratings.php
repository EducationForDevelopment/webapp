<?php


    $rating = new ratings($_POST['widget_id']);


    isset($_POST['fetch']) ? $rating->get_ratings() : $rating->vote();






class ratings {

    #var $data_file = './ratings.data.txt';
    var $data_file = './ratings_data.txt';
    private $widget_id;
    private $data = array();


function __construct($wid) {

    $this->widget_id = $wid;

    $all = file_get_contents($this->data_file);

    if($all) {
        $this->data = unserialize($all);
    }
}
public function get_ratings() {
    if($this->data[$this->widget_id]) {
        echo json_encode($this->data[$this->widget_id]);
    }
    else {
        $data['widget_id'] = $this->widget_id;
        $data['number_votes'] = 0;
        $data['total_points'] = 0;
        $data['dec_avg'] = 0;
        $data['whole_avg'] = 0;
        echo json_encode($data);
    }
}
public function vote() {

    # Get the value of the vote
    preg_match('/star_([1-5]{1})/', $_POST['clicked_on'], $match);
    $vote = $match[1];

    $ID = $this->widget_id;
    # Update the record if it exists
    if($this->data[$ID]) {
        $this->data[$ID]['number_votes'] += 1;
        $this->data[$ID]['total_points'] += $vote;
    }
    # Create a new one if it doesn't
    else {
        $this->data[$ID]['number_votes'] = 1;
        $this->data[$ID]['total_points'] = $vote;
    }

    $this->data[$ID]['dec_avg'] = round( $this->data[$ID]['total_points'] / $this->data[$ID]['number_votes'], 1 );
    $this->data[$ID]['whole_avg'] = round( $this->data[$ID]['dec_avg'] );


    file_put_contents($this->data_file, serialize($this->data));
    $this->get_ratings();
}

# ---
# end class
}














//function return_rating($raw_id) {
//
//    $widget_data = fetch_rating($raw_id);
//    echo json_encode($widget_data);
//}
//
//# Data is stored as:
//#     widget_id:number_of_voters:total_points:dec_avg:whole_avg
//function fetch_rating($raw_id) {
//
//    $all  = file('./ratings.data.txt');
//
//    foreach($all as $k => $record) {
//        if(preg_match("/$raw_id:/", $record)) {
//            $selected = $all[$k];
//            break;
//        }
//    }
//
//    if($selected) {
//        $data = split(':', $selected);
//        $data[] = round( $data[2] / $data[1], 1 );
//        $data[] = round( $data[3] );
//    }
//    else {
//        $data[0] = $raw_id;
//        $data[1] = 0;
//        $data[2] = 0;
//        $data[3] = 0;
//        $data[4] = 0;
//    }
//
//    return $data;
//}
//
//
//
//
//function register_vote() {
//
//    preg_match('/star_([1-5]{1})/', $_POST['clicked_on'], $match);
//    $vote = $match[1];
//
//    $current_data = fetch_rating($_POST['widget']);
//
//    $new_data[] = $current_data['stars'] + $vote;
//    $new_data[] = $current_data['cast'] + 1;
//
//
//    # --> This needs to be fixed, since a widget ID is ALWAYS passed in
//    # it should be a class property
//    file_put_contents($_POST['widget'] . '.txt', "{$new_data[0]}\n{$new_data[1]}");
//
//    return_rating($_POST['widget']);
//}

    //foreach($all as $k => $record) {
    //    if(preg_match("/$raw_id:/", $record)) {
    //        $selected = $all[$k];
    //        break;
    //    }
    //}
    //
    //if($selected) {
    //    $this->data = split(':', $selected);
    //    $this->data[] = round( $this->data[2] / $this->data[1], 1 );
    //    $this->data[] = round( $this->data[3] );
    //}
    //else {
    //    $this->data[0] = $this->widget_id;
    //    $this->data[1] = 0;
    //    $this->data[2] = 0;
    //    $this->data[3] = 0;
    //    $this->data[4] = 0;
    //}
?>
