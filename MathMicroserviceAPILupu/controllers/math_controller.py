from flask import Blueprint, request, jsonify, current_app
from services.math_service import compute_factorial, compute_power, compute_fibonacci
from models.request_log import RequestLog

# Allowed operations for filtering logs
ALLOWED_OPERATIONS = {"factorial", "power", "fibonacci"}

# Create a Blueprint (modular way to define routes)
math_bp = Blueprint('math', __name__)

@math_bp.route('/factorial', methods=['POST'])
def factorial():
    data = request.get_json()

    if not data or 'n' not in data:
        return jsonify({"error": "Missing 'n' in request"}), 400

    try:
        n = int(data['n'])
        if n < 0:
            return jsonify({"error": "n must be a non-negative integer"}), 400

        result = compute_factorial(n)

        # Log the request to the database
        session = current_app.session_factory()
        log = RequestLog(
            operation="factorial",
            input_data=str({"n": n}),
            result=result
        )
        session.add(log)
        session.commit()
        session.close()

        return jsonify({
            "operation": "factorial",
            "input": n,
            "result": result
        })

    except ValueError:
        return jsonify({"error": "'n' must be an integer"}), 400

@math_bp.route('/pow', methods=['POST'])
def power():
    data = request.get_json()

    if not data or 'a' not in data or 'b' not in data:
        return jsonify({"error": "Missing 'a' or 'b' in request"}), 400

    try:
        a = float(data['a'])
        b = float(data['b'])
        result = compute_power(a, b)

        # Log the request to the database
        session = current_app.session_factory()
        log = RequestLog(
            operation="power",
            input_data=str({"a": a, "b": b}),
            result=result
        )
        session.add(log)
        session.commit()
        session.close()

        return jsonify({
            "operation": "power",
            "input": {"a": a, "b": b},
            "result": result
        })

    except ValueError:
        return jsonify({"error": "'a' and 'b' must be numbers"}), 400

@math_bp.route('/fibonacci', methods=['POST'])
def fibonacci():
    data = request.get_json()

    if not data or 'n' not in data:
        return jsonify({"error": "Missing 'n' in request"}), 400

    try:
        n = int(data['n'])
        if n < 0:
            return jsonify({"error": "n must be a non-negative integer"}), 400

        result = compute_fibonacci(n)

        # Log the request to the database
        session = current_app.session_factory()
        log = RequestLog(
            operation="fibonacci",
            input_data=str({"n": n}),
            result=result
        )
        session.add(log)
        session.commit()
        session.close()

        return jsonify({
            "operation": "fibonacci",
            "input": n,
            "result": result
        })

    except ValueError:
        return jsonify({"error": "'n' must be an integer"}), 400


@math_bp.route('/logs', methods=['GET'])
def get_logs():
    session = current_app.session_factory()

    # Read query parameters
    operation_filter = request.args.get('operation')
    page = request.args.get('page', default=1, type=int)

    if page < 1:
        session.close()
        return jsonify({"error": "Page number must be 1 or greater."}), 400

    limit = 10
    offset = (page - 1) * limit

    query = session.query(RequestLog)

    if operation_filter:
        if operation_filter not in ALLOWED_OPERATIONS:
            session.close()
            return jsonify({
                "error": f"Invalid operation '{operation_filter}'. Must be one of: {', '.join(ALLOWED_OPERATIONS)}"
            }), 400
        query = query.filter(RequestLog.operation == operation_filter)

    # Add pagination
    logs = query.order_by(RequestLog.timestamp.desc()).offset(offset).limit(limit).all()
    session.close()

    log_list = []
    for log in logs:
        log_list.append({
            "operation": log.operation,
            "input_data": log.input_data,
            "result": log.result,
            "timestamp": log.timestamp.isoformat()
        })

    return jsonify({
        "page": page,
        "logs": log_list
    })



import csv
import io
from flask import Response


@math_bp.route('/logs/export', methods=['GET'])
def export_logs():
    import csv
    import io
    from flask import Response, request

    session = current_app.session_factory()

    # Optional filtering
    operation_filter = request.args.get("operation")

    query = session.query(RequestLog)

    if operation_filter:
        if operation_filter not in ALLOWED_OPERATIONS:
            session.close()
            return jsonify({
                "error": f"Invalid operation '{operation_filter}'. Must be one of: {', '.join(ALLOWED_OPERATIONS)}"
            }), 400
        query = query.filter(RequestLog.operation == operation_filter)

    logs = query.order_by(RequestLog.timestamp.desc()).all()
    session.close()

    # CSV creation
    output = io.StringIO()
    writer = csv.writer(output)

    writer.writerow(["operation", "input_data", "result", "timestamp"])

    for log in logs:
        writer.writerow([
            log.operation,
            log.input_data,
            log.result,
            log.timestamp.isoformat()
        ])

    # Build CSV download response
    filename = f"logs_{operation_filter if operation_filter else 'all'}.csv"
    response = Response(output.getvalue(), mimetype='text/csv')
    response.headers.set("Content-Disposition", "attachment", filename=filename)
    return response


@math_bp.route('/logs/export.json', methods=['GET'])
def export_logs_json():
    session = current_app.session_factory()
    logs = session.query(RequestLog).order_by(RequestLog.timestamp.desc()).all()
    session.close()

    # Convert logs to list of dictionaries
    log_list = []
    for log in logs:
        log_list.append({
            "operation": log.operation,
            "input_data": log.input_data,
            "result": log.result,
            "timestamp": log.timestamp.isoformat()
        })

    # Convert list to JSON string
    json_data = jsonify(log_list)

    # Build response with JSON as downloadable file
    response = Response(json_data.get_data(), mimetype='application/json')
    response.headers.set("Content-Disposition", "attachment", filename="logs.json")
    return response
