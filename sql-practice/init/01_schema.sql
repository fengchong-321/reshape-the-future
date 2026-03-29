-- 物流系统练习数据库

-- 1. 客户表
CREATE TABLE customers (
    customer_id INT PRIMARY KEY AUTO_INCREMENT,
    name VARCHAR(50) NOT NULL,
    phone VARCHAR(20),
    city VARCHAR(50)
);

-- 2. 包裹表
CREATE TABLE packages (
    package_id INT PRIMARY KEY AUTO_INCREMENT,
    tracking_number VARCHAR(20) UNIQUE NOT NULL,
    sender_id INT NOT NULL,
    receiver_id INT NOT NULL,
    weight DECIMAL(6,2) COMMENT '公斤',
    declared_value DECIMAL(10,2) COMMENT '声明价值',
    create_time DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (sender_id) REFERENCES customers(customer_id),
    FOREIGN KEY (receiver_id) REFERENCES customers(customer_id)
);

-- 3. 运输状态表（记录每个包裹的运输节点）
CREATE TABLE shipments (
    shipment_id INT PRIMARY KEY AUTO_INCREMENT,
    package_id INT NOT NULL,
    status VARCHAR(20) NOT NULL COMMENT '状态: pick_up, in_transit, delivered, exception',
    location VARCHAR(100),
    update_time DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (package_id) REFERENCES packages(package_id)
);
