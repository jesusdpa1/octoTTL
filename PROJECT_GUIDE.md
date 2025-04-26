# OctoTTL: A Real-Time Experimental Framework for Electrophysiology

## Project Vision

OctoTTL is a next-generation experimental framework designed to handle real-time electrophysiology data streams with high performance, low latency, and flexible extensibility. The framework transitions from the original CardiacLab codebase to a more modular, stream-processing architecture that can support multiple types of input devices, data processing algorithms, and control outputs.

The name "OctoTTL" reflects both the eight-armed flexibility of the system (like an octopus) and its ability to control multiple TTL (Transistor-Transistor Logic) outputs in parallel for experimental control.

## Core Design Principles

1. **Stream-First Architecture**: All data flows through the system as continuous streams rather than discrete batches
2. **Zero-Copy Operations**: Minimize data copying between components using PyArrow's memory model
3. **Pluggable Components**: Any component can be swapped out with a compatible alternative
4. **Real-Time Performance**: Processing and control decisions happen with predictable, low latency
5. **Type-Safe Data Flow**: Strong typing of data at all stages for reliability
6. **Parallel Processing**: Utilize multi-core capabilities for performance
7. **Resilient Operation**: Graceful handling of errors and recovery from failures
8. **Extensible Interfaces**: Clear interfaces for adding new devices, processors, and controllers

## Architectural Overview

OctoTTL is organized around the concept of a data flow pipeline with clear separation of concerns:

```
Input Devices → Data Streams → Processors → Controllers → Output Devices
      ↓             ↓             ↓             ↓             ↓
  (DSI, etc.)  (PyArrow/Polars) (Analysis)  (Experiment)   (Arduino)
      ↓                                                      ↓
Storage ←───────────────────────────────────────────────── Logs
```

The system uses Apache Arrow as the underlying memory model, with Polars providing high-performance data operations, and a stream processing model inspired by Apache Spark and Kafka Streams for handling continuous data.

## Key Innovations

1. **Unified Memory Model with PyArrow**: All data is stored and processed in Apache Arrow format, eliminating costly conversions between stages of the pipeline.

2. **Polars-Based Stream Processing**: Using Polars as the processing engine provides near-native performance through its Rust implementation and parallel execution.

3. **Real-Time Storage**: Data is stored continuously without blocking the processing pipeline, using time-partitioned Parquet files with Zstandard compression.

4. **Pluggable Data Sources**: The framework can accept data from any source that can be converted to the Arrow format, making it adaptable to many experimental setups.

5. **State Machine Experiment Control**: A formal state machine manages the experiment flow, ensuring predictable transitions between stages.

## System Components

### 1. Communication Streams

OctoTTL supports multiple communication protocols for data acquisition and device control, each with specific characteristics, advantages, and limitations.

#### Ethernet Stream

The Ethernet Stream module supports network-based data acquisition and control:

**Key Features:**
- **High Bandwidth**: Support for high data throughput (10/100/1000 Mbps)
- **TCP/IP and UDP**: Support for both reliable (TCP) and low-latency (UDP) protocols
- **Socket Programming**: Low-level socket interfaces for custom protocols
- **ZeroMQ Integration**: Advanced message queuing for distributed systems
- **Arrow Flight**: High-performance data transfer using Arrow Flight protocol
- **Remote Monitoring**: Access experiment data from remote locations
- **Device Discovery**: Automatic discovery of compatible devices on the network
- **Security**: Authentication and encryption options
- **Quality of Service**: Prioritize critical control messages

**Supported Protocols:**
- **TCP/IP**: Reliable, connection-oriented communication
- **UDP**: Low-latency, connectionless communication
- **WebSockets**: Bi-directional, full-duplex communication
- **MQTT**: Lightweight messaging protocol for IoT devices
- **ZeroMQ**: Advanced message queuing
- **Arrow Flight**: High-performance data transfer using Arrow format

#### Serial Stream

The Serial Stream module supports traditional serial communication for device control and data acquisition:

**Key Features:**
- **Universal Compatibility**: Works with most laboratory equipment
- **Multiple Standards**: Support for RS-232, RS-485, USB-Serial, etc.
- **Buffer Management**: Efficient handling of serial data buffers
- **Framing Protocol**: Robust message framing and error detection
- **Flow Control**: Hardware and software flow control options
- **Baudrate Negotiation**: Automatic baudrate detection and negotiation
- **Protocol Abstraction**: Expose data as streams regardless of underlying protocol
- **Error Recovery**: Automatic recovery from communication errors
- **Debugging Tools**: Analysis tools for serial communication issues

**Supported Protocols:**
- **RS-232/RS-485**: Standard serial protocols
- **USB-Serial**: Serial over USB
- **Bluetooth Serial**: Serial over Bluetooth
- **FTDI/CP210x**: Common USB-Serial chipsets
- **Custom Binary**: Support for custom binary protocols
- **ASCII/Text**: Support for text-based protocols

#### Specialized Hardware Streams

OctoTTL can be extended to support specialized data acquisition hardware:

**Key Features:**
- **DAQ Cards**: Support for data acquisition cards (National Instruments, etc.)
- **Custom Hardware**: Integration with custom data acquisition hardware
- **FPGA Integration**: Support for FPGA-based systems
- **Real-time Systems**: Integration with real-time operating systems
- **High-speed Acquisition**: Support for high-speed data acquisition
- **Multi-channel Data**: Handle multi-channel data streams
- **Time Synchronization**: Precise timing synchronization between channels
- **Hardware Triggering**: Support for hardware-based triggering
- **Calibration**: Automatic calibration of analog signals

These communication streams form the foundation of OctoTTL's data acquisition and control capabilities, providing a flexible and extensible platform for integrating diverse hardware into a cohesive experimental system.

### 2. Communications Module

The Communications module provides interfaces to various external devices and data sources.

#### Key Features:

- **Device Abstraction**: All hardware devices are accessed through abstract interfaces
- **Asynchronous I/O**: Non-blocking communication with all devices
- **Protocol Implementation**: Hardware-specific protocol implementations
- **Streaming Interface**: All devices provide data as continuous streams
- **Error Handling**: Robust error handling and recovery for device communication
- **Arrow Flight Integration**: Support for remote data access via Arrow Flight

#### Supported Devices (Extendable):

- **DSI Systems**: Communication with physiological monitoring systems
- **Arduino**: Control of TTL outputs for experimental manipulation
- **Generic Serial**: Support for any serial-based custom hardware
- **Network Devices**: Support for networked data acquisition systems

### 2. Processors Module

The Processors module handles all transformations and analyses on the data streams.

#### Key Features:

- **Stream Transformations**: Functions for mapping, filtering, and transforming data streams
- **Windowing Operations**: Time and count-based sliding windows over streams
- **Statistical Analysis**: Commonly-used statistical calculations on streaming data
- **Signal Processing**: Physiological signal-specific processing algorithms
- **Threshold Detection**: Detection of threshold crossings and pattern recognition
- **Multi-Channel Support**: Process multiple data channels simultaneously
- **Parallel Execution**: Efficient use of available CPU cores

#### Core Processor Types:

- **StreamProcessor**: Base class for all stream processing components
- **WindowProcessor**: Apply operations on sliding windows of data
- **FilterProcessor**: Filter data points based on criteria
- **StatisticsProcessor**: Calculate statistics on streaming data
- **ThresholdProcessor**: Detect threshold crossings and generate events
- **SignalProcessor**: Apply signal processing algorithms to physiological data

### 3. Data Models Module

The Data Models module defines the core data structures and schemas used throughout the system.

#### Key Features:

- **Arrow Schemas**: Define the structure of all data used in the system
- **Schema Registry**: Central repository of all available schemas
- **Type Safety**: Ensure type consistency across the pipeline
- **Data Validation**: Validate data against schemas
- **Extensibility**: Easy addition of new data types
- **Configuration Models**: Define experiment and device configurations
- **Stream Models**: Define the behavior of data streams

#### Core Components:

- **Base Schemas**: Foundation schemas for time-series data
- **Device-Specific Schemas**: Schemas for specific input devices (DSI, etc.)
- **Configuration Schema**: Schema for experiment configuration
- **Stream Definitions**: Definitions for stream behavior
- **Event Models**: Models for system events and triggers

### 4. Controllers Module

The Controllers module manages the overall experimental flow and coordinates system components.

#### Key Features:

- **State Machine**: Formal state machine for experiment flow
- **Experiment Configuration**: Load and validate experiment configurations
- **Component Coordination**: Coordinate all system components
- **Error Handling**: Manage system-wide error handling
- **Logging**: Comprehensive logging of experiment flow
- **User Interface**: Integration with user interface
- **Remote Control**: Support for remote control of experiments

#### Core Components:

- **ExperimentController**: Main controller for experiment execution
- **StateMachine**: State machine for experiment flow
- **ConfigurationManager**: Manage experiment configurations
- **ComponentRegistry**: Registry of all active system components
- **ErrorHandler**: System-wide error handling
- **LogManager**: Manage system logs

### 5. Storage Module

The Storage module handles the efficient storage and retrieval of experimental data.

#### Key Features:

- **Non-Blocking Storage**: Store data without blocking the processing pipeline
- **Time-Partitioned Storage**: Organize data by time for efficient access
- **Compression**: Use efficient compression to reduce storage requirements
- **Metadata Storage**: Store experiment metadata alongside data
- **Query Interface**: Efficient query interface for data retrieval
- **Export Capabilities**: Export data in various formats
- **Data Management**: Tools for managing stored data

#### Core Components:

- **StreamStorage**: Storage engine for streaming data
- **ParquetWriter**: Write data to Parquet files
- **QueryEngine**: Engine for querying stored data
- **ExportManager**: Manage data export
- **MetadataStore**: Store and retrieve experiment metadata
- **StorageManager**: Manage storage resources

### 6. Utils Module

The Utils module provides common utilities used throughout the system.

#### Key Features:

- **Time Management**: Utilities for time handling
- **Configuration Handling**: Utilities for configuration handling
- **Logging**: Comprehensive logging utilities
- **Error Handling**: Error handling utilities
- **Concurrency Utilities**: Utilities for concurrent operations
- **Testing Utilities**: Utilities for testing

#### Core Components:

- **TimeManager**: Utilities for time handling
- **ConfigUtil**: Utilities for configuration handling
- **LogUtil**: Logging utilities
- **ErrorUtil**: Error handling utilities
- **ConcurrencyUtil**: Concurrency utilities
- **TestUtil**: Testing utilities

## Data Models

The Data Models section defines the fundamental data structures that flow through the OctoTTL system. These models serve as the common language between different system components, ensuring consistent interpretation of data throughout the processing pipeline.

### Core Data Models

#### Time-Series Data

The foundation of electrophysiology data is time-series measurements:

- **Sample Model**: Represents a single data point with timestamp
- **Channel Model**: Represents a stream of samples from a specific source
- **Frame Model**: Groups multiple samples across channels at the same timestamp
- **Signal Model**: Represents a continuous signal with metadata
- **Event Model**: Represents point-in-time events within a signal

#### Metadata Models

Metadata provides context for interpreting the raw data:

- **Experiment Metadata**: Information about the experiment setup
- **Subject Metadata**: Information about the experimental subject
- **Channel Metadata**: Information about specific data channels
- **Calibration Metadata**: Calibration information for raw signals
- **Annotation Metadata**: Human or automated annotations on signals

#### Configuration Models

Configuration models define system behavior:

- **Device Configuration**: Configuration for input/output devices
- **Processor Configuration**: Configuration for signal processors
- **Threshold Configuration**: Configuration for threshold detection
- **Storage Configuration**: Configuration for data storage
- **Controller Configuration**: Configuration for experimental control

### Schema Evolution

Data models can evolve over time without breaking existing systems:

- **Versioned Schemas**: All schemas are versioned
- **Compatibility Rules**: Rules for schema compatibility
- **Schema Registry**: Central repository of schemas
- **Schema Validation**: Validation of data against schemas
- **Conversion Utilities**: Utilities for converting between schema versions

## Integration Strategy

OctoTTL adopts a stream processing model that draws inspiration from successful systems like Apache Spark Streaming and Kafka Streams, but is tailored specifically for real-time electrophysiology data.

Key integration approaches include:

1. **Stream Processing Pipeline**:
   - Data flows through the system as continuous streams
   - Each component in the pipeline can transform the stream
   - Components can be chained together to form a processing pipeline
   - Processing happens in a distributed, parallel manner

2. **Event-Driven Architecture**:
   - Components communicate via events
   - Events trigger state transitions
   - Events can be logged for later analysis
   - Events can trigger actions in the physical world

3. **Pluggable Component Model**:
   - Components are defined by interfaces
   - Components can be replaced with compatible alternatives
   - New components can be added without modifying existing code
   - Components can be tested in isolation

## Implementation Roadmap

### Phase 1: Core Infrastructure

1. Define core interfaces and data models
2. Implement basic stream processing engine
3. Implement storage engine
4. Create DSI device adapter as reference implementation
5. Implement basic Arduino controller

### Phase 2: Processing Capabilities

1. Implement windowing operations
2. Add statistical processing
3. Create threshold detection
4. Develop signal processing algorithms
5. Implement real-time visualization

### Phase 3: Experiment Control

1. Implement state machine for experiment flow
2. Create experiment configuration system
3. Develop logging and monitoring
4. Add error handling and recovery
5. Create user interface for experiment control

### Phase 4: Extension and Optimization

1. Add support for additional devices
2. Optimize performance
3. Add data export features
4. Create data analysis tools
5. Develop documentation and examples

## Extending OctoTTL

One of the primary design goals of OctoTTL is extensibility. Researchers should be able to adapt the framework to their specific needs without modifying the core codebase.

### Adding New Devices

To add a new input device:

1. Create a new class implementing the `InputDevice` interface
2. Define the device's data schema
3. Implement the device's protocol
4. Register the device with the system

### Adding New Processors

To add a new data processor:

1. Create a new class implementing the `Processor` interface
2. Define the processor's input and output schemas
3. Implement the processing logic
4. Register the processor with the system

### Adding New Controllers

To add a new controller:

1. Create a new class implementing the `Controller` interface
2. Define the controller's state machine
3. Implement the control logic
4. Register the controller with the system

## Performance Considerations

OctoTTL is designed for high-performance real-time processing. Key performance considerations include:

1. **Memory Management**: Use Arrow's zero-copy operations
2. **Parallel Processing**: Utilize all available CPU cores
3. **Bounded Memory**: Use windowing to limit memory usage
4. **Asynchronous I/O**: Non-blocking I/O for all operations
5. **Efficient Storage**: Compress data efficiently
6. **Selective Processing**: Process only necessary data
7. **Resource Monitoring**: Monitor and manage resource usage

## Data Security and Integrity

Ensuring data security and integrity is critical:

1. **Data Validation**: Validate all data against schemas
2. **Error Detection**: Detect and handle errors
3. **Data Checksums**: Use checksums to verify data integrity
4. **Data Encryption**: Encrypt sensitive data
5. **Access Control**: Control access to data
6. **Audit Logging**: Log all system activities
7. **Recovery Mechanisms**: Recover from failures

## Conclusion

OctoTTL represents a significant advancement in real-time experimental frameworks for electrophysiology. By adopting modern stream processing techniques and leveraging high-performance libraries like PyArrow and Polars, OctoTTL provides a flexible, extensible platform for a wide range of experimental designs.

The transition from CardiacLab to OctoTTL marks a shift from batch-oriented, tightly-coupled code to a stream-oriented, loosely-coupled architecture that can adapt to a wide range of experimental requirements while maintaining high performance and reliability.
