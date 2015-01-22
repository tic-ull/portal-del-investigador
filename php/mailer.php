<?php

// Set the recipient email address.
// FIXME: Update this to your desired email address.
$recipient_email = "<recipient_address>";

// Set the source email address.
$source_name = "<source_name>";
$source_email = "<source_email>";

// Set the email subject.
$subject = "<email_subject> from %s";

//
// http://php.net/manual/en/function.http-response-code.php#107261
//

if (!function_exists('http_response_code')) {
    function http_response_code($code = NULL) {
        if ($code !== NULL) {
            switch ($code) {
                case 100: $text = 'Continue'; break;
                case 101: $text = 'Switching Protocols'; break;
                case 200: $text = 'OK'; break;
                case 201: $text = 'Created'; break;
                case 202: $text = 'Accepted'; break;
                case 203: $text = 'Non-Authoritative Information'; break;
                case 204: $text = 'No Content'; break;
                case 205: $text = 'Reset Content'; break;
                case 206: $text = 'Partial Content'; break;
                case 300: $text = 'Multiple Choices'; break;
                case 301: $text = 'Moved Permanently'; break;
                case 302: $text = 'Moved Temporarily'; break;
                case 303: $text = 'See Other'; break;
                case 304: $text = 'Not Modified'; break;
                case 305: $text = 'Use Proxy'; break;
                case 400: $text = 'Bad Request'; break;
                case 401: $text = 'Unauthorized'; break;
                case 402: $text = 'Payment Required'; break;
                case 403: $text = 'Forbidden'; break;
                case 404: $text = 'Not Found'; break;
                case 405: $text = 'Method Not Allowed'; break;
                case 406: $text = 'Not Acceptable'; break;
                case 407: $text = 'Proxy Authentication Required'; break;
                case 408: $text = 'Request Time-out'; break;
                case 409: $text = 'Conflict'; break;
                case 410: $text = 'Gone'; break;
                case 411: $text = 'Length Required'; break;
                case 412: $text = 'Precondition Failed'; break;
                case 413: $text = 'Request Entity Too Large'; break;
                case 414: $text = 'Request-URI Too Large'; break;
                case 415: $text = 'Unsupported Media Type'; break;
                case 500: $text = 'Internal Server Error'; break;
                case 501: $text = 'Not Implemented'; break;
                case 502: $text = 'Bad Gateway'; break;
                case 503: $text = 'Service Unavailable'; break;
                case 504: $text = 'Gateway Time-out'; break;
                case 505: $text = 'HTTP Version not supported'; break;
                default:
                    exit('Unknown http status code "' . htmlentities($code) . '"');
                break;
            }

            $protocol = (isset($_SERVER['SERVER_PROTOCOL']) ? $_SERVER['SERVER_PROTOCOL'] : 'HTTP/1.0');

            header($protocol . ' ' . $code . ' ' . $text);
            $GLOBALS['http_response_code'] = $code;

        } else {
            $code = (isset($GLOBALS['http_response_code']) ? $GLOBALS['http_response_code'] : 200);
        }

        return $code;

    }
}

//
// http://blog.teamtreehouse.com/create-ajax-contact-form
//

// Only process POST requests.
if ($_SERVER["REQUEST_METHOD"] == "POST") {
    // Get the form fields and remove whitespace.
    $name = strip_tags(trim($_POST["name"]));
    $name = str_replace(array("\r","\n"),array(" "," "),$name);
    $email = filter_var(trim($_POST["email"]), FILTER_SANITIZE_EMAIL);
    $message = trim($_POST["message"]);
    $sendcopy = ($_POST["sendcopy"] == "sendcopy") ? true : false;
    $honeypot = $_POST["honeypot"];

    // Check that data was sent to the mailer.
    if ( (! empty($honeypot)) OR empty($name) OR empty($message) OR !filter_var($email, FILTER_VALIDATE_EMAIL)) {
        // Set a 400 (bad request) response code and exit.
        http_response_code(400);
        echo "<strong>Oops!</strong> There was a problem with your submission. Please complete the form and try again.";
        exit;
    }

    mb_internal_encoding('UTF-8');

    // Set the email subject.
    $subject = mb_encode_mimeheader(sprintf($subject, $name), 'UTF-8', 'Q');

    // Build the email content.
    $email_content = "Name: $name\n";
    $email_content .= "Email: $email\n\n";
    $email_content .= "Message:\n$message\n";

    // Build the email headers.
    $email_headers = array();
    $email_headers[] = 'MIME-Version: 1.0';
    $email_headers[] = 'Content-type: text/plain; charset=UTF-8';
    $email_headers[] = "From: " . mb_encode_mimeheader("$source_name", 'UTF-8', 'Q') . "<$source_email>";
    if ( $sendcopy ) {
        $email_headers[] = "Cc: " . mb_encode_mimeheader("$name", 'UTF-8', 'Q') . "<$email>";
    }

    // Send the email.
    if (mail($recipient_email, $subject, $email_content, implode("\r\n", $email_headers))) {
        // Set a 200 (okay) response code.
        http_response_code(200);
        echo "<strong>Thanks for contacting us!</strong> We will get back to you as soon as possible.";
    } else {
        // Set a 500 (internal server error) response code.
        http_response_code(500);
        echo "<strong>Oops!</strong> Something went wrong and we couldn't send your message.";
    }

} else {
    // Not a POST request, set a 403 (forbidden) response code.
    http_response_code(403);
    echo "<strong>Oops!</strong> There was a problem with your submission, please try again.";
}
